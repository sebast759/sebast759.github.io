#!/usr/bin/env python3
"""Fare monitor: Ericeira → Lisbon Airport (LIS). Primary: bolt.eu | Fallback: uber.com"""

import asyncio
import csv
import re
import time
import random
from datetime import datetime
from pathlib import Path
from typing import Optional

import schedule
from playwright.async_api import async_playwright, TimeoutError as PWTimeout

# ── Route ──────────────────────────────────────────────────────────────────────
PICKUP_ADDR   = "Ericeira, Portugal"
DROPOFF_ADDR  = "Aeroporto de Lisboa"
PICKUP_LAT,  PICKUP_LNG  = 38.9617, -9.4179
DROPOFF_LAT, DROPOFF_LNG = 38.7742, -9.1342

# ── Schedule ───────────────────────────────────────────────────────────────────
SCHEDULED_HOURS = [6, 8, 10, 13, 16, 18, 20, 23]

# ── Output ─────────────────────────────────────────────────────────────────────
CSV_FILE    = Path("fares.csv")
CSV_HEADERS = ["timestamp", "hour", "service_tier", "price_eur", "currency", "source"]

_CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)


# ── CSV helpers ────────────────────────────────────────────────────────────────

def ensure_csv() -> None:
    if not CSV_FILE.exists():
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(CSV_HEADERS)


def append_rows(rows: list[dict]) -> None:
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=CSV_HEADERS).writerows(rows)


# ── Price parsing ──────────────────────────────────────────────────────────────

def parse_price(text: str) -> Optional[float]:
    """Return float from '€12.50', '10–15 €', '12,50', etc. Ranges → midpoint."""
    t = re.sub(r"[€$£\s ]", "", text.replace(",", "."))
    m = re.search(r"([\d.]+)[–\-]([\d.]+)", t)
    if m:
        return round((float(m.group(1)) + float(m.group(2))) / 2, 2)
    m = re.search(r"\d+\.\d+|\d+", t)
    return float(m.group()) if m else None


# ── JSON tree search ───────────────────────────────────────────────────────────

def _hunt_fares(obj, out: list, source: str, ts: str, hour: int, _depth: int = 0) -> None:
    """Recursively scan any JSON structure for {name, price} fare pairs."""
    if _depth > 12 or not isinstance(obj, (dict, list)):
        return
    if isinstance(obj, dict):
        name = (
            obj.get("name") or obj.get("category") or obj.get("vehicle_type")
            or obj.get("service_name") or obj.get("product_name")
        )
        raw = (
            obj.get("price") or obj.get("fare") or obj.get("estimated_price")
            or obj.get("min_price") or obj.get("price_estimate")
            or obj.get("total_fare") or obj.get("upfront_fare_amount")
        )
        if name and raw is not None:
            if isinstance(raw, dict):
                amount   = raw.get("amount") or raw.get("value")
                currency = raw.get("currency_code") or raw.get("currency", "EUR")
            elif isinstance(raw, (int, float)):
                amount   = raw
                currency = obj.get("currency_code") or obj.get("currency", "EUR")
            else:
                amount   = parse_price(str(raw))
                currency = "EUR"
            if amount is not None:
                out.append({
                    "timestamp":    ts,
                    "hour":         hour,
                    "service_tier": str(name).strip(),
                    "price_eur":    round(float(amount), 2),
                    "currency":     str(currency),
                    "source":       source,
                })
        for v in obj.values():
            _hunt_fares(v, out, source, ts, hour, _depth + 1)
    else:
        for item in obj:
            _hunt_fares(item, out, source, ts, hour, _depth + 1)


# ── Shared helpers ─────────────────────────────────────────────────────────────

async def _jitter(lo: float = 5.0, hi: float = 15.0) -> None:
    await asyncio.sleep(random.uniform(lo, hi))


async def _accept_cookies(page) -> None:
    """Dismiss GDPR / cookie consent banners if present."""
    for sel in [
        'button:has-text("Accept all")',
        'button:has-text("Accept")',
        'button:has-text("I agree")',
        'button[id*="accept" i]',
        '[data-testid*="accept-cookies" i]',
    ]:
        try:
            btn = page.locator(sel).first
            if await btn.is_visible(timeout=1_500):
                await btn.click()
                await _jitter(0.5, 1.0)
                return
        except Exception:
            pass


async def _first_selector(page, selectors: list[str], timeout_ms: int = 2_000):
    """Return the first matching element found across a list of CSS selectors."""
    for sel in selectors:
        try:
            return await page.wait_for_selector(sel, timeout=timeout_ms)
        except PWTimeout:
            pass
    return None


async def _click_first_suggestion(page) -> None:
    """Click the top autocomplete suggestion if one appears."""
    for sel in ['[role="option"]', 'li[role="option"]', '[data-testid*="suggestion"]', '.autocomplete-result']:
        try:
            sug = await page.wait_for_selector(sel, timeout=3_000)
            await sug.click()
            await _jitter(0.5, 1.0)
            return
        except PWTimeout:
            pass


# ── Bolt.eu scraper ────────────────────────────────────────────────────────────

async def scrape_bolt(ctx) -> list[dict]:
    ts, hour = datetime.now().isoformat(timespec="seconds"), datetime.now().hour
    captured: list[dict] = []
    page = await ctx.new_page()

    # Intercept every JSON response from bolt.eu – catches the fare API call
    # before it ever renders to the DOM.
    async def on_resp(resp):
        if "bolt.eu" not in resp.url:
            return
        if "json" not in resp.headers.get("content-type", ""):
            return
        try:
            _hunt_fares(await resp.json(), captured, "bolt.eu", ts, hour)
        except Exception:
            pass

    page.on("response", on_resp)

    try:
        await page.goto(
            "https://bolt.eu/en-pt/rides/",
            wait_until="domcontentloaded",
            timeout=30_000,
        )
        await _accept_cookies(page)
        await _jitter(2, 4)

        pickup = await _first_selector(page, [
            'input[placeholder*="pickup" i]',
            'input[placeholder*="from" i]',
            'input[placeholder*="where from" i]',
            '[data-testid*="pickup"] input',
            '[data-testid="origin-input"]',
            'input[name="pickup"]',
        ])

        if pickup is None:
            print("[bolt] booking form not found – bolt.eu may require app/login")
            return []

        await pickup.click()
        await pickup.type(PICKUP_ADDR, delay=80)
        await _jitter(1, 2)
        await _click_first_suggestion(page)

        dropoff = await _first_selector(page, [
            'input[placeholder*="dropoff" i]',
            'input[placeholder*="destination" i]',
            'input[placeholder*="where to" i]',
            'input[placeholder*="to" i]',
            '[data-testid*="dropoff"] input',
            '[data-testid="destination-input"]',
            'input[name="dropoff"]',
        ])

        if dropoff:
            await dropoff.click()
            await dropoff.type(DROPOFF_ADDR, delay=80)
            await _jitter(1, 2)
            await _click_first_suggestion(page)

        await _jitter(3, 5)

        # DOM fallback: scan rendered service-tier cards
        if not captured:
            cards = await page.query_selector_all(
                '[class*="category" i], [class*="service-type" i], '
                '[class*="vehicle-type" i], [data-testid*="tier"]'
            )
            for card in cards:
                try:
                    n_el = await card.query_selector('[class*="name" i], [class*="title" i], h4, strong')
                    p_el = await card.query_selector('[class*="price" i], [class*="fare" i]')
                    name  = (await n_el.inner_text()).strip() if n_el else None
                    price = parse_price(await p_el.inner_text()) if p_el else None
                    if name and price:
                        captured.append({
                            "timestamp": ts, "hour": hour,
                            "service_tier": name, "price_eur": price,
                            "currency": "EUR", "source": "bolt.eu",
                        })
                except Exception:
                    pass

    except Exception as e:
        print(f"[bolt] {e}")
    finally:
        await page.close()

    print(f"[bolt] {len(captured)} fare(s)" if captured else "[bolt] no fares captured")
    return captured


# ── Uber fallback scraper ──────────────────────────────────────────────────────

async def scrape_uber(ctx) -> list[dict]:
    ts, hour = datetime.now().isoformat(timespec="seconds"), datetime.now().hour
    results: list[dict] = []
    page = await ctx.new_page()

    async def on_resp(resp):
        if "uber.com" not in resp.url:
            return
        if "json" not in resp.headers.get("content-type", ""):
            return
        try:
            _hunt_fares(await resp.json(), results, "uber.com", ts, hour)
        except Exception:
            pass

    page.on("response", on_resp)

    try:
        url = (
            "https://www.uber.com/global/en/price-estimate/"
            f"?pickup_lat={PICKUP_LAT}&pickup_lng={PICKUP_LNG}"
            f"&dropoff_lat={DROPOFF_LAT}&dropoff_lng={DROPOFF_LNG}"
        )
        await page.goto(url, wait_until="networkidle", timeout=40_000)
        await _accept_cookies(page)
        await _jitter(3, 6)

        # DOM fallback if network interception found nothing
        if not results:
            cards = await page.query_selector_all(
                '[data-testid*="price-estimate"], [class*="PriceEstimate"], '
                '[class*="price-estimate-product"], [class*="ProductCard"]'
            )
            for card in cards:
                try:
                    n_el = await card.query_selector(
                        '[class*="ProductName"], [class*="product-name"], '
                        '[data-testid="product-name"], h3'
                    )
                    p_el = await card.query_selector(
                        '[class*="PriceRange"], [class*="price-range"], '
                        '[data-testid="price-range"]'
                    )
                    name  = (await n_el.inner_text()).strip() if n_el else None
                    price = parse_price(await p_el.inner_text()) if p_el else None
                    if name and price:
                        results.append({
                            "timestamp": ts, "hour": hour,
                            "service_tier": name, "price_eur": price,
                            "currency": "EUR", "source": "uber.com",
                        })
                except Exception:
                    pass

    except Exception as e:
        print(f"[uber] {e}")
    finally:
        await page.close()

    print(f"[uber] {len(results)} fare(s)" if results else "[uber] no fares captured")
    return results


# ── Orchestrator ───────────────────────────────────────────────────────────────

async def _run() -> None:
    print(f"\n── {datetime.now():%Y-%m-%d %H:%M} ── scraping …")
    rows: list[dict] = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        ctx = await browser.new_context(
            user_agent=_CHROME_UA,
            viewport={"width": 1280, "height": 800},
            locale="en-US",
            timezone_id="Europe/Lisbon",
        )

        rows.extend(await scrape_bolt(ctx))
        await _jitter(5, 15)
        rows.extend(await scrape_uber(ctx))

        await browser.close()

    if rows:
        append_rows(rows)
        print(f"── saved {len(rows)} row(s) → {CSV_FILE}")
    else:
        print("── no data captured this run")


def _job() -> None:
    asyncio.run(_run())


# ── Entry point ────────────────────────────────────────────────────────────────

def main() -> None:
    ensure_csv()
    for h in SCHEDULED_HOURS:
        schedule.every().day.at(f"{h:02d}:00").do(_job)

    print(f"Bolt fare scraper | {PICKUP_ADDR} → {DROPOFF_ADDR}")
    print(f"Schedule: {SCHEDULED_HOURS}:00 local  |  output: {CSV_FILE.resolve()}")
    print("Starting first run …\n")
    _job()

    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
