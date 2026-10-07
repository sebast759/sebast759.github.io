"""
Nightly rate scraper for The Hoxton, Shepherd's Bush (1 night, 2 adults, 1 room).

Run locally (written blind from a sandbox with no network access, so not yet run against live pages).

Setup:
  pip install playwright pandas beautifulsoup4
  playwright install chromium

Commands:
  python scrape_rates.py probe-hoxton
      Opens a visible browser on The Hoxton site. Run ONE search by hand
      (any date, 2 adults, 1 room). Press Enter in the terminal when rates show.
      Saves every JSON/XHR response to raw/hoxton_probe/ so the official
      booking engine adapter can be written from real payloads.

  python scrape_rates.py scrape-booking [--headed] [--start 2026-10-08] [--end 2027-04-07]
      Fetches one Booking.com page per arrival date and saves raw HTML to raw/booking/.
      Resumable: dates already saved are skipped. Delete a file to re-fetch it.

  python scrape_rates.py parse-booking
      Parses saved HTML (no network) into:
        hoxton_shepherds_bush_daily_rates.csv  one row per date, spec columns
        hoxton_all_rate_rows.csv               every room/rate row seen, for audit
      Failed or ambiguous pages are left with an empty price and an error note
      in hoxton_all_rate_rows.csv. Nothing is interpolated.
"""

import argparse
import json
import random
import re
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
BOOKING_DIR = RAW / "booking"
PROBE_DIR = RAW / "hoxton_probe"
MANIFEST = RAW / "booking_manifest.jsonl"

START = date(2026, 10, 8)
END = date(2027, 4, 7)

HOXTON_URL = "https://thehoxton.com/london/shepherds-bush/hotels/"
# Slug unverified from the sandbox. Open it once in a normal browser; fix here if it redirects elsewhere.
BOOKING_URL = "https://www.booking.com/hotel/gb/the-hoxton-shepherds-bush.html"

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

MONEY_RE = re.compile(r"£\s?([\d,]+(?:\.\d{1,2})?)")
SOLD_OUT_PATTERNS = [
    "no availability",
    "sold out",
    "no rooms available",
    "we have no availability",
    "not available on our site",
]
BLOCK_PATTERNS = ["captcha", "are you a robot", "verify you are human", "access denied"]
PROMO_PATTERNS = ["genius", "deal", "discount", "% off", "limited-time", "early booker", "late escape", "mobile-only", "member"]


def daterange(start: date, end: date):
    d = start
    while d <= end:
        yield d
        d += timedelta(days=1)


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def parse_money(text: str | None) -> float | None:
    if not text:
        return None
    m = MONEY_RE.search(text.replace("\xa0", " "))
    return float(m.group(1).replace(",", "")) if m else None


# --------------------------------------------------------------------------- probe


def probe_hoxton() -> None:
    from playwright.sync_api import sync_playwright

    PROBE_DIR.mkdir(parents=True, exist_ok=True)
    captured = []

    def on_response(resp):
        try:
            ctype = resp.headers.get("content-type", "")
            rtype = resp.request.resource_type
            if "json" in ctype or rtype in ("xhr", "fetch"):
                body = resp.text()
                captured.append(
                    {
                        "url": resp.url,
                        "status": resp.status,
                        "method": resp.request.method,
                        "post_data": resp.request.post_data,
                        "content_type": ctype,
                        "body": body[:2_000_000],
                    }
                )
        except Exception as exc:  # body may be unavailable for redirects
            captured.append({"url": resp.url, "error": repr(exc)})

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        ctx = browser.new_context(user_agent=USER_AGENT, locale="en-GB", timezone_id="Europe/London")
        page = ctx.new_page()
        page.on("response", on_response)
        page.goto(HOXTON_URL, wait_until="domcontentloaded")
        input("Run one search in the browser (2 adults, 1 room, 1 night). When rates are visible, press Enter here... ")
        final_url = page.url
        (PROBE_DIR / "final_page.html").write_text(page.content(), encoding="utf-8")
        page.screenshot(path=str(PROBE_DIR / "final_page.png"), full_page=True)
        browser.close()

    (PROBE_DIR / "responses.json").write_text(json.dumps(captured, indent=1), encoding="utf-8")
    (PROBE_DIR / "final_url.txt").write_text(final_url, encoding="utf-8")
    print(f"Saved {len(captured)} responses to {PROBE_DIR}. Final URL: {final_url}")
    print("Share responses.json, final_url.txt and final_page.png (or the relevant JSON) to build the official adapter.")


# --------------------------------------------------------------------------- booking.com fetch


def booking_url(d: date) -> str:
    return (
        f"{BOOKING_URL}?checkin={d.isoformat()}&checkout={(d + timedelta(days=1)).isoformat()}"
        "&group_adults=2&group_children=0&no_rooms=1&selected_currency=GBP&lang=en-gb"
    )


def scrape_booking(start: date, end: date, headed: bool, min_delay: float, max_delay: float) -> None:
    from playwright.sync_api import TimeoutError as PWTimeout
    from playwright.sync_api import sync_playwright

    BOOKING_DIR.mkdir(parents=True, exist_ok=True)
    todo = [d for d in daterange(start, end) if not (BOOKING_DIR / f"{d.isoformat()}.html").exists()]
    print(f"{len(todo)} dates to fetch")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not headed)
        ctx = browser.new_context(
            user_agent=USER_AGENT, locale="en-GB", timezone_id="Europe/London", viewport={"width": 1400, "height": 1000}
        )
        page = ctx.new_page()
        consecutive_blocks = 0

        for i, d in enumerate(todo, 1):
            url = booking_url(d)
            status, err = "ok", None
            try:
                page.goto(url, wait_until="domcontentloaded", timeout=60_000)
                try:
                    page.click("#onetrust-accept-btn-handler", timeout=3_000)
                except PWTimeout:
                    pass
                try:
                    page.wait_for_selector("table.hprt-table, #no_availability_msg, .sold_out_property", timeout=20_000)
                except PWTimeout:
                    status = "no_table_or_message"
                html = page.content()
            except Exception as exc:
                status, err, html = "fetch_error", repr(exc), None

            low = (html or "").lower()
            if html and any(p in low for p in BLOCK_PATTERNS) and "hprt-table" not in low:
                status = "blocked"
                consecutive_blocks += 1
            else:
                consecutive_blocks = 0

            # Blocked or failed pages are not saved as HTML, so a rerun retries them.
            if html and status != "blocked":
                (BOOKING_DIR / f"{d.isoformat()}.html").write_text(html, encoding="utf-8")

            with MANIFEST.open("a", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        {"date": d.isoformat(), "ts": now_iso(), "status": status, "error": err, "url": url, "final_url": page.url}
                    )
                    + "\n"
                )
            print(f"[{i}/{len(todo)}] {d} {status}")

            if consecutive_blocks >= 3:
                print("Blocked 3 times in a row. Stopping. Rerun later, ideally with --headed, to resume.")
                break
            time.sleep(random.uniform(min_delay, max_delay))

        browser.close()


# --------------------------------------------------------------------------- booking.com parse


def classify_refundable(text: str) -> bool | None:
    t = text.lower()
    if "non-refundable" in t or "non refundable" in t:
        return False
    if "free cancellation" in t or "refundable" in t:
        return True
    return None


def parse_booking_html(html: str) -> tuple[list[dict], str | None, bool]:
    """Return (rate_rows, error, sold_out)."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    table = soup.select_one("table.hprt-table")
    page_text = soup.get_text(" ", strip=True).lower()

    if table is None:
        if soup.select_one("#no_availability_msg, .sold_out_property") or any(p in page_text for p in SOLD_OUT_PATTERNS):
            return [], None, True
        return [], "no rate table and no sold out message", False

    rows, current_room = [], None
    for tr in table.select("tbody tr"):
        name_el = tr.select_one(".hprt-roomtype-icon-link, .hprt-roomtype-link, [data-room-name]")
        if name_el is not None:
            current_room = name_el.get_text(" ", strip=True) or name_el.get("data-room-name")

        price_el = tr.select_one(".bui-price-display__value, .prco-valign-middle-helper, .hprt-price-price")
        if price_el is None:
            continue
        price = parse_money(price_el.get_text(" ", strip=True))

        tax_el = tr.select_one(".prd-taxes-and-fees-under-price, .hprt-price-taxes")
        tax_text = tax_el.get_text(" ", strip=True) if tax_el else ""
        taxes = parse_money(tax_text)
        taxes_included = "includes taxes" in tax_text.lower() or "included" in tax_text.lower()

        cond_el = tr.select_one(".hprt-table-cell-conditions, .hprt-conditions")
        cond_text = cond_el.get_text(" ", strip=True) if cond_el else ""

        orig_el = tr.select_one(".bui-price-display__original, .prco-ltr-right-align-helper s, del")
        row_text = tr.get_text(" ", strip=True).lower()
        promo_hits = [p for p in PROMO_PATTERNS if p in row_text]
        promotion = bool(orig_el) or bool(promo_hits)

        rows.append(
            {
                "room_type": current_room,
                "price_gbp": price,
                "refundable": classify_refundable(cond_text),
                "taxes_gbp": taxes if not taxes_included else 0.0,
                "taxes_text": tax_text,
                "conditions": cond_text,
                "original_price_gbp": parse_money(orig_el.get_text(" ", strip=True)) if orig_el else None,
                "promotion": promotion,
                "promotion_detail": ";".join(promo_hits),
            }
        )

    if not rows:
        return [], "rate table found but no priced rows parsed", False
    return rows, None, False


def load_manifest() -> dict:
    latest = {}
    if MANIFEST.exists():
        for line in MANIFEST.read_text(encoding="utf-8").splitlines():
            rec = json.loads(line)
            latest[rec["date"]] = rec
    return latest


def parse_booking(start: date, end: date) -> None:
    manifest = load_manifest()
    daily, audit = [], []

    for d in daterange(start, end):
        key = d.isoformat()
        rec = manifest.get(key, {})
        base = {
            "date": key,
            "day_of_week": d.strftime("%A"),
            "price_gbp": None,
            "refundable_price_gbp": None,
            "room_type": None,
            "taxes_gbp": None,
            "promotion": None,
            "sold_out": None,
            "source": "booking.com",
            "scrape_timestamp": rec.get("ts"),
        }
        path = BOOKING_DIR / f"{key}.html"
        if not path.exists():
            audit.append({"date": key, "error": f"not fetched ({rec.get('status', 'never attempted')})"})
            base["source"] = None
            daily.append(base)
            continue

        rows, err, sold_out = parse_booking_html(path.read_text(encoding="utf-8"))
        if err:
            audit.append({"date": key, "error": err})
            daily.append(base)
            continue
        if sold_out:
            base["sold_out"] = True
            audit.append({"date": key, "sold_out": True})
            daily.append(base)
            continue

        for r in rows:
            audit.append({"date": key, **r})

        priced = [r for r in rows if r["price_gbp"] is not None]
        if not priced:
            audit.append({"date": key, "error": "rows found but no price parsed"})
            daily.append(base)
            continue

        cheapest = min(priced, key=lambda r: r["price_gbp"])
        refundable = [r for r in priced if r["refundable"] is True]
        cheapest_ref = min(refundable, key=lambda r: r["price_gbp"]) if refundable else None

        base.update(
            {
                "price_gbp": cheapest["price_gbp"],
                "refundable_price_gbp": cheapest_ref["price_gbp"] if cheapest_ref else None,
                "room_type": cheapest["room_type"],
                "taxes_gbp": cheapest["taxes_gbp"],
                "promotion": cheapest["promotion"],
                "sold_out": False,
            }
        )
        daily.append(base)

    cols = [
        "date", "day_of_week", "price_gbp", "refundable_price_gbp", "room_type",
        "taxes_gbp", "promotion", "sold_out", "source", "scrape_timestamp",
    ]
    out = pd.DataFrame(daily)[cols]
    out.to_csv(ROOT / "hoxton_shepherds_bush_daily_rates.csv", index=False)
    pd.DataFrame(audit).to_csv(ROOT / "hoxton_all_rate_rows.csv", index=False)

    n_price = out["price_gbp"].notna().sum()
    n_sold = (out["sold_out"] == True).sum()  # noqa: E712
    n_miss = len(out) - n_price - n_sold
    print(f"{len(out)} dates: {n_price} priced, {n_sold} sold out, {n_miss} missing")
    if n_miss:
        print("Missing dates are listed with reasons in hoxton_all_rate_rows.csv (error column).")


# --------------------------------------------------------------------------- cli


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("probe-hoxton")
    s = sub.add_parser("scrape-booking")
    s.add_argument("--headed", action="store_true")
    s.add_argument("--min-delay", type=float, default=5.0)
    s.add_argument("--max-delay", type=float, default=11.0)
    for p in (s, sub.add_parser("parse-booking")):
        p.add_argument("--start", type=date.fromisoformat, default=START)
        p.add_argument("--end", type=date.fromisoformat, default=END)
    args = ap.parse_args()

    if args.cmd == "probe-hoxton":
        probe_hoxton()
    elif args.cmd == "scrape-booking":
        scrape_booking(args.start, args.end, args.headed, args.min_delay, args.max_delay)
    elif args.cmd == "parse-booking":
        parse_booking(args.start, args.end)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
