#!/usr/bin/env python3
"""
BTC liquidations: trend following or reversal?

Data source: Coinalyze public API (free key at https://coinalyze.net/account/api-key/).
  * Liquidations: long and short liquidated notional in USD, summed over every BTC
    perpetual listed on Coinalyze (Binance, Bybit, OKX, Deribit, ...).
  * Price: Binance BTCUSDT perpetual OHLCV (BTCUSDT_PERP.A), same bar grid.

Retention caveat: Coinalyze keeps a limited number of intraday bars per interval,
while daily history goes back years. Run several intervals to trade resolution
against sample size.

Sign convention used everywhere in the report:
  imb = (short_liq - long_liq) / (short_liq + long_liq)
  imb > 0: shorts got liquidated (forced buying, squeeze up)
  imb < 0: longs got liquidated (forced selling, flush down)
  "reversal score" = forward return signed AGAINST the liquidation flow.
  reversal score > 0  => reversal ; < 0 => trend following.

Usage:
  export COINALYZE_API_KEY=xxxx
  python btc_liquidations_study.py --intervals 1hour 4hour daily
  python btc_liquidations_study.py --intervals 1hour --refresh --z-thr 2.5 --fee-bps 5 --entry-lag 1

Outputs (next to this script):
  data/    cached raw pulls (csv.gz)
  output/  report_<interval>.md + png charts
"""
from __future__ import annotations

import argparse
import os
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import statsmodels.api as sm

BASE_URL = "https://api.coinalyze.net/v1"
PRICE_SYMBOL = "BTCUSDT_PERP.A"
INTERVAL_SECONDS = {
    "1min": 60, "5min": 300, "15min": 900, "30min": 1800,
    "1hour": 3600, "2hour": 7200, "4hour": 14400, "6hour": 21600,
    "12hour": 43200, "daily": 86400,
}
HORIZONS_HOURS = [1, 4, 12, 24, 72, 168]
HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
OUT_DIR = HERE / "output"

COLOR_LONG = "#eb6834"   # long liquidations (forced selling)
COLOR_SHORT = "#2a78d6"  # short liquidations (forced buying)
INK = "#3d3d3a"
GRID = "#e4e3dc"


# ============================================================ API

class Coinalyze:
    def __init__(self, api_key: str, min_spacing: float = 1.6):
        self.session = requests.Session()
        self.session.headers["api_key"] = api_key
        self.min_spacing = min_spacing  # free tier: 40 calls / minute
        self._last = 0.0

    def get(self, endpoint: str, params: dict | None = None):
        for attempt in range(8):
            wait = self.min_spacing - (time.monotonic() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.monotonic()
            r = self.session.get(f"{BASE_URL}/{endpoint}", params=params, timeout=30)
            if r.status_code == 429:
                time.sleep(float(r.headers.get("Retry-After", 5)) + 0.5)
                continue
            if r.status_code >= 500:
                time.sleep(2 ** attempt)
                continue
            r.raise_for_status()
            return r.json()
        raise RuntimeError(f"Coinalyze /{endpoint} failed after retries: {params}")


def btc_perp_symbols(client: Coinalyze) -> list[str]:
    markets = client.get("future-markets")
    syms = sorted(
        m["symbol"] for m in markets
        if m.get("base_asset") == "BTC" and m.get("is_perpetual")
    )
    if PRICE_SYMBOL not in syms:
        raise RuntimeError(f"{PRICE_SYMBOL} not found in Coinalyze future-markets")
    return syms


def fetch_history(client: Coinalyze, endpoint: str, symbols: list[str], interval: str,
                  start_ts: int, end_ts: int, extra: dict | None = None,
                  chunk_bars: int = 500) -> pd.DataFrame:
    """Walk backwards from end_ts in chunks; stop at the first empty chunk (retention edge)."""
    step = INTERVAL_SECONDS[interval] * chunk_bars
    rows: list[dict] = []
    to_ts = end_ts
    while to_ts > start_ts:
        from_ts = max(start_ts, to_ts - step)
        n_before = len(rows)
        for i in range(0, len(symbols), 20):  # max 20 symbols per call
            params = {"symbols": ",".join(symbols[i:i + 20]), "interval": interval,
                      "from": from_ts, "to": to_ts, **(extra or {})}
            for item in client.get(endpoint, params):
                for h in item.get("history", []):
                    rows.append({"symbol": item["symbol"], **h})
        print(f"  {endpoint} {interval} "
              f"{pd.Timestamp(from_ts, unit='s'):%Y-%m-%d} -> {pd.Timestamp(to_ts, unit='s'):%Y-%m-%d}: "
              f"+{len(rows) - n_before} rows")
        if len(rows) == n_before:
            break
        to_ts = from_ts - 1
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    df["t"] = pd.to_datetime(df["t"], unit="s", utc=True)
    return df.drop_duplicates(["symbol", "t"]).sort_values(["symbol", "t"]).reset_index(drop=True)


def load_or_fetch(name: str, fetch_fn, refresh: bool) -> pd.DataFrame:
    path = DATA_DIR / f"{name}.csv.gz"
    if path.exists() and not refresh:
        df = pd.read_csv(path)
        if "t" in df.columns:
            df["t"] = pd.to_datetime(df["t"], utc=True)
        return df
    df = fetch_fn()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return df


# ============================================================ PANEL + FEATURES

def build_panel(liq_raw: pd.DataFrame, px_raw: pd.DataFrame, interval: str) -> pd.DataFrame:
    sec = INTERVAL_SECONDS[interval]
    liq = (liq_raw.groupby("t")[["l", "s"]].sum()
           .rename(columns={"l": "long_liq", "s": "short_liq"}))
    px = (px_raw[px_raw["symbol"] == PRICE_SYMBOL].set_index("t")[["o", "h", "l", "c", "v"]]
          .rename(columns={"o": "open", "h": "high", "l": "low", "c": "close", "v": "volume"}))
    start = max(liq.index.min(), px.index.min())
    end = min(liq.index.max(), px.index.max())
    grid = pd.date_range(start, end, freq=f"{sec}s", tz="UTC")
    df = px.reindex(grid).join(liq.reindex(grid))
    df["close"] = df["close"].ffill()
    df[["long_liq", "short_liq"]] = df[["long_liq", "short_liq"]].fillna(0.0)
    return df.iloc[:-1]  # last bar may still be open


def rolling_z(x: pd.Series, window: int) -> pd.Series:
    m = x.rolling(window, min_periods=window // 2).mean().shift(1)
    s = x.rolling(window, min_periods=window // 2).std().shift(1)
    return (x - m) / s


def horizons_in_bars(interval: str) -> list[int]:
    sec = INTERVAL_SECONDS[interval]
    return sorted({max(1, int(round(hh * 3600 / sec))) for hh in HORIZONS_HOURS})


def add_features(df: pd.DataFrame, interval: str, window_days: float, vol_halflife_days: float,
                 horizons: list[int], entry_lag: int) -> pd.DataFrame:
    bpd = 86400 / INTERVAL_SECONDS[interval]
    window = max(int(round(window_days * bpd)), 60)
    halflife = max(vol_halflife_days * bpd, 10)
    out = df.copy()
    out["ret"] = np.log(out["close"]).diff()
    vol_t = out["ret"].ewm(halflife=halflife, min_periods=window // 2).std()  # known at close t
    out["vol_t"] = vol_t
    out["ret_z"] = out["ret"] / vol_t.shift(1)  # bar return in ex ante sigma units

    L, S = out["long_liq"], out["short_liq"]
    tot = L + S
    out["z_long"] = rolling_z(np.log1p(L), window)
    out["z_short"] = rolling_z(np.log1p(S), window)
    out["z_tot"] = rolling_z(np.log1p(tot), window)
    out["imb"] = ((S - L) / tot).where(tot > 0, 0.0)
    out["liq_sig"] = out["imb"] * out["z_tot"].clip(lower=0)  # signed liquidation intensity

    logc = np.log(out["close"])
    for h in horizons:
        fwd = logc.shift(-(h + entry_lag)) - logc.shift(-entry_lag)
        out[f"fwd_{h}"] = fwd
        out[f"fwdz_{h}"] = fwd / (vol_t * np.sqrt(h))
    return out


# ============================================================ ANALYSES

def decluster(mask: pd.Series, gap: int) -> pd.Series:
    keep = np.zeros(len(mask), dtype=bool)
    last = -10 ** 12
    for i in np.flatnonzero(mask.fillna(False).to_numpy()):
        if i - last >= gap:
            keep[i] = True
            last = i
    return pd.Series(keep, index=mask.index)


def event_masks(out: pd.DataFrame, thr: float, gap: int) -> dict[str, pd.Series]:
    long_ev = (out["z_long"] > thr) & (out["imb"] < 0)
    short_ev = (out["z_short"] > thr) & (out["imb"] > 0)
    return {"long_liq_spike": decluster(long_ev, gap), "short_liq_spike": decluster(short_ev, gap)}


def hac_mean_test(y: pd.Series, dummy: pd.Series, maxlags: int) -> tuple[float, float]:
    """Excess mean of y when dummy != 0 vs the rest, HAC (Newey West) t stat for overlap."""
    d = pd.concat([y, dummy.astype(float)], axis=1).dropna()
    if d.iloc[:, 1].abs().sum() < 5:
        return np.nan, np.nan
    res = sm.OLS(d.iloc[:, 0], sm.add_constant(d.iloc[:, 1])).fit(
        cov_type="HAC", cov_kwds={"maxlags": maxlags})
    return float(res.params.iloc[1]), float(res.tvalues.iloc[1])


def event_study(out: pd.DataFrame, events: dict[str, pd.Series], horizons: list[int]) -> pd.DataFrame:
    rows = []
    for h in horizons:
        fwd, fwdz = out[f"fwd_{h}"], out[f"fwdz_{h}"]
        uncond_bps = fwd.mean() * 1e4
        signed_dummy = pd.Series(0.0, index=out.index)
        for name, mask in events.items():
            sign = 1.0 if name == "long_liq_spike" else -1.0  # reversal direction
            signed_dummy[mask] = sign
            x, xz = fwd[mask].dropna(), fwdz[mask].dropna()
            excess_z, t = hac_mean_test(fwdz, mask, maxlags=h)
            rows.append({
                "event": name, "h_bars": h, "n": len(x),
                "bar_ret_bps": out.loc[mask, "ret"].mean() * 1e4,
                "mean_fwd_bps": x.mean() * 1e4, "uncond_bps": uncond_bps,
                "median_fwd_bps": x.median() * 1e4, "hit_up": (x > 0).mean(),
                "mean_fwd_sigma": xz.mean(), "excess_sigma": excess_z, "t_hac": t,
            })
        # pooled reversal score: fwdz ~ const + signed dummy (+1 long spike, -1 short spike).
        # The constant absorbs drift; b > 0 => reversal, b < 0 => trend.
        rev = (fwdz * signed_dummy).where(signed_dummy != 0)
        b, t = hac_mean_test(fwdz, signed_dummy, maxlags=h)
        rows.append({
            "event": "POOLED reversal score", "h_bars": h, "n": int(rev.notna().sum()),
            "bar_ret_bps": np.nan, "mean_fwd_bps": np.nan, "uncond_bps": np.nan,
            "median_fwd_bps": np.nan, "hit_up": (rev.dropna() > 0).mean(),
            "mean_fwd_sigma": rev.mean(), "excess_sigma": b, "t_hac": t,
        })
    return pd.DataFrame(rows)


def regressions(out: pd.DataFrame, horizons: list[int]) -> pd.DataFrame:
    """fwdz_h ~ ret_z + liq_sig. b_liq > 0 => trend, < 0 => reversal (controlling for price move)."""
    rows = []
    n = len(out)
    samples = {"full": out, "1st_half": out.iloc[: n // 2], "2nd_half": out.iloc[n // 2:]}
    for h in horizons:
        for sname, d0 in samples.items():
            d = d0[[f"fwdz_{h}", "ret_z", "liq_sig"]].replace([np.inf, -np.inf], np.nan).dropna()
            if len(d) < 100:
                continue
            y = d[f"fwdz_{h}"]
            m1 = sm.OLS(y, sm.add_constant(d[["liq_sig"]])).fit(cov_type="HAC", cov_kwds={"maxlags": h})
            m2 = sm.OLS(y, sm.add_constant(d[["ret_z", "liq_sig"]])).fit(cov_type="HAC", cov_kwds={"maxlags": h})
            rows.append({
                "h_bars": h, "sample": sname, "n": len(d),
                "b_liq_alone": m1.params["liq_sig"], "t_liq_alone": m1.tvalues["liq_sig"],
                "b_liq_ctrl": m2.params["liq_sig"], "t_liq_ctrl": m2.tvalues["liq_sig"],
                "b_ret": m2.params["ret_z"], "t_ret": m2.tvalues["ret_z"],
                "r2_pct": m2.rsquared * 100,
            })
    return pd.DataFrame(rows)


def imbalance_buckets(out: pd.DataFrame, horizons: list[int], z_min: float = 1.0, q: int = 5) -> pd.DataFrame:
    """Among bars with elevated liquidations, bucket imbalance and average fwd sigma return."""
    d = out[out["z_tot"] > z_min].copy()
    if len(d) < q * 10:
        return pd.DataFrame()
    d["bucket"] = pd.qcut(d["imb"].rank(method="first"), q, labels=[f"Q{i + 1}" for i in range(q)])
    agg = {"imb": "mean", "ret_z": "mean"}
    agg.update({f"fwdz_{h}": "mean" for h in horizons})
    res = d.groupby("bucket", observed=True).agg(agg)
    res.insert(0, "n", d.groupby("bucket", observed=True).size())
    return res.rename(columns={f"fwdz_{h}": f"fwd_sigma_h{h}" for h in horizons})


def strategy(out: pd.DataFrame, interval: str, h: int, thr: float, fee_bps: float,
             entry_lag: int, mode: str) -> dict:
    """Staggered h tranches: signal at close t, trade from t+1+lag, hold h bars."""
    raw = np.where(out["z_tot"] > thr, -np.sign(out["imb"]), 0.0)
    if mode == "trend":
        raw = -raw
    sig = pd.Series(raw, index=out.index).rolling(h, min_periods=1).mean()
    pos = sig.shift(1 + entry_lag).fillna(0.0)
    gross = pos * out["ret"].fillna(0.0)
    net = gross - fee_bps / 1e4 * pos.diff().abs().fillna(0.0)
    ann = np.sqrt(86400 / INTERVAL_SECONDS[interval] * 365)

    def stats(p: pd.Series) -> tuple[float, float, float]:
        sr = p.mean() / p.std() * ann if p.std() > 0 else np.nan
        eq = p.cumsum()
        return sr, p.mean() * ann ** 2 * 100, (eq - eq.cummax()).min() * 100

    sr_g, ret_g, _ = stats(gross)
    sr_n, ret_n, dd_n = stats(net)
    return {"mode": mode, "h_bars": h, "sharpe_gross": sr_g, "sharpe_net": sr_n,
            "ann_ret_gross_pct": ret_g, "ann_ret_net_pct": ret_n, "max_dd_net_pct": dd_n,
            "time_in_mkt_pct": (pos != 0).mean() * 100,
            "turnover_per_yr": pos.diff().abs().sum() / (len(pos) / ann ** 2)}


# ============================================================ PLOTS

def _style(ax):
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(GRID)
    ax.tick_params(colors=INK, labelsize=9)


def plot_event_paths(out: pd.DataFrame, events: dict[str, pd.Series], interval: str, path: Path):
    bpd = 86400 / INTERVAL_SECONDS[interval]
    post = int(min(max(3 * bpd, 10), 120))
    pre = post // 2
    logc = np.log(out["close"]).to_numpy()
    ks = np.arange(-pre, post + 1)
    fig, ax = plt.subplots(figsize=(9, 5))
    for name, color, label in [("long_liq_spike", COLOR_LONG, "Long liquidation spike"),
                               ("short_liq_spike", COLOR_SHORT, "Short liquidation spike")]:
        idx = np.flatnonzero(events[name].to_numpy())
        idx = idx[(idx - pre >= 0) & (idx + post < len(logc))]
        if len(idx) < 5:
            continue
        paths = np.array([logc[i + ks] - logc[i] for i in idx]) * 1e4
        mu = np.nanmean(paths, axis=0)
        se = np.nanstd(paths, axis=0) / np.sqrt(len(idx))
        ax.fill_between(ks, mu - 1.96 * se, mu + 1.96 * se, color=color, alpha=0.15, linewidth=0)
        ax.plot(ks, mu, color=color, linewidth=2, label=f"{label} (n={len(idx)})")
        ax.annotate(label, (ks[-1], mu[-1]), xytext=(4, 0), textcoords="offset points",
                    color=INK, fontsize=9, va="center")
    ax.axvline(0, color=INK, linewidth=0.8)
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.set_xlabel(f"bars from event ({interval}); 0 = close of the liquidation bar", color=INK)
    ax.set_ylabel("cumulative log return (bps), 95% CI", color=INK)
    ax.set_title(f"BTC path around liquidation spikes, {interval}", color=INK, loc="left")
    _style(ax)
    ax.legend(frameon=False, fontsize=9, loc="upper left")
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def plot_buckets(buckets: pd.DataFrame, h: int, interval: str, path: Path):
    col = f"fwd_sigma_h{h}"
    if buckets.empty or col not in buckets:
        return
    fig, ax = plt.subplots(figsize=(7, 4))
    vals = buckets[col].to_numpy()
    ax.bar(buckets.index.astype(str), vals, color=COLOR_SHORT, width=0.6)
    for i, v in enumerate(vals):
        ax.annotate(f"{v:+.3f}", (i, v), xytext=(0, 3 if v >= 0 else -12),
                    textcoords="offset points", ha="center", fontsize=9, color=INK)
    ax.axhline(0, color=INK, linewidth=0.8)
    ax.set_xlabel("imbalance quintile (Q1 = longs liquidated, Q5 = shorts liquidated)", color=INK)
    ax.set_ylabel(f"mean fwd return, sigma units, h={h} bars", color=INK)
    ax.set_title(f"Forward return by liquidation imbalance, {interval}, z_tot > 1",
                 color=INK, loc="left")
    _style(ax)
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


# ============================================================ REPORT

def md_table(df: pd.DataFrame, floatfmt: str = "{:.3f}") -> str:
    df = df.reset_index() if df.index.name or not isinstance(df.index, pd.RangeIndex) else df
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in df.iterrows():
        cells = []
        for v in r.to_numpy():
            if isinstance(v, (float, np.floating)):
                cells.append("" if np.isnan(v) else floatfmt.format(v))
            else:
                cells.append(str(v))
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def verdict(ev: pd.DataFrame) -> str:
    pooled = ev[ev["event"] == "POOLED reversal score"]
    lines = []
    for _, r in pooled.iterrows():
        t = r["t_hac"]
        if np.isnan(t):
            tag = "not enough events"
        elif t > 2:
            tag = "REVERSAL (significant)"
        elif t < -2:
            tag = "TREND (significant)"
        else:
            tag = "inconclusive"
        lines.append(f"* h={int(r['h_bars'])} bars: score {r['excess_sigma']:+.3f} sigma, "
                     f"t={t:+.2f}, n={int(r['n'])} -> {tag}")
    return "\n".join(lines)


def run_interval(client: Coinalyze | None, symbols: list[str], interval: str, args) -> None:
    print(f"\n=== {interval} ===")
    end_ts = int(time.time())
    start_ts = int(pd.Timestamp(args.start, tz="UTC").timestamp())
    liq_raw = load_or_fetch(
        f"liq_{interval}",
        lambda: fetch_history(client, "liquidation-history", symbols, interval, start_ts, end_ts,
                              extra={"convert_to_usd": "true"}),
        args.refresh)
    px_raw = load_or_fetch(
        f"ohlcv_{interval}",
        lambda: fetch_history(client, "ohlcv-history", [PRICE_SYMBOL], interval, start_ts, end_ts),
        args.refresh)
    if liq_raw.empty or px_raw.empty:
        print(f"  no data for {interval}, skipped")
        return

    horizons = horizons_in_bars(interval)
    df = build_panel(liq_raw, px_raw, interval)
    out = add_features(df, interval, args.window_days, args.vol_halflife_days, horizons, args.entry_lag)
    out = out[out["z_tot"].notna() & out["vol_t"].notna()]
    gap = max(1, int(round(args.decluster_hours * 3600 / INTERVAL_SECONDS[interval])))
    events = event_masks(out, args.z_thr, gap)

    ev = event_study(out, events, horizons)
    reg = regressions(out, horizons)
    buckets = imbalance_buckets(out, horizons)
    strat = pd.DataFrame([strategy(out, interval, h, args.z_thr, args.fee_bps, args.entry_lag, mode)
                          for h in horizons for mode in ("reversal", "trend")])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    mid_h = horizons[len(horizons) // 2]
    plot_event_paths(out, events, interval, OUT_DIR / f"event_paths_{interval}.png")
    plot_buckets(buckets, mid_h, interval, OUT_DIR / f"imbalance_buckets_{interval}.png")

    n_sym = liq_raw["symbol"].nunique()
    report = f"""# BTC liquidations: trend or reversal ({interval})

Sample: {out.index.min():%Y-%m-%d %H:%M} to {out.index.max():%Y-%m-%d %H:%M} UTC, {len(out)} bars.
Liquidations summed over {n_sym} BTC perpetuals (USD). Price: {PRICE_SYMBOL}.
Params: z_thr={args.z_thr}, z window={args.window_days}d, decluster gap={gap} bars,
entry lag={args.entry_lag} bar(s), fee={args.fee_bps} bps per unit turnover.
Horizons (bars): {horizons}.

## Verdict (pooled reversal score, HAC t stat)

Score = forward return in sigma units signed against the liquidation flow.
Positive = price reverts after the forced flow, negative = it keeps going.

{verdict(ev)}

## Event study

long_liq_spike: z(long liq) > thr and longs dominate (forced selling).
short_liq_spike: z(short liq) > thr and shorts dominate (forced buying).
excess_sigma / t_hac: conditional minus unconditional mean of the sigma normalised
forward return, Newey West with lags = h.

{md_table(ev)}

![event paths](event_paths_{interval}.png)

## Regressions: fwd_sigma(h) ~ ret_z + liq_sig

liq_sig = imb * max(z_tot, 0). b_liq > 0 means trend, < 0 means reversal.
b_liq_ctrl controls for the bar's own price move, which separates the liquidation
effect from plain short term price momentum or reversal.

{md_table(reg)}

## Imbalance quintiles (bars with z_tot > 1)

Monotonic increase from Q1 to Q5 = trend; decrease = reversal.

{md_table(buckets)}

![imbalance buckets](imbalance_buckets_{interval}.png)

## Toy strategy

Signal at bar close when z_tot > thr, direction against (reversal) or with (trend)
the dominant liquidation side, h staggered tranches, no leverage, fees on turnover.
Not a backtest you should trust: in sample, no slippage model, no funding.

{md_table(strat)}
"""
    (OUT_DIR / f"report_{interval}.md").write_text(report)
    print(verdict(ev))
    print(f"  report: {OUT_DIR / f'report_{interval}.md'}")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--intervals", nargs="+", default=["1hour", "4hour", "daily"],
                   choices=list(INTERVAL_SECONDS))
    p.add_argument("--start", default="2019-01-01")
    p.add_argument("--z-thr", type=float, default=2.0)
    p.add_argument("--window-days", type=float, default=30.0)
    p.add_argument("--vol-halflife-days", type=float, default=7.0)
    p.add_argument("--decluster-hours", type=float, default=24.0)
    p.add_argument("--entry-lag", type=int, default=0)
    p.add_argument("--fee-bps", type=float, default=4.0)
    p.add_argument("--refresh", action="store_true", help="ignore cache and refetch")
    args = p.parse_args()

    key = os.environ.get("COINALYZE_API_KEY")
    need_fetch = args.refresh or any(
        not (DATA_DIR / f"{k}_{i}.csv.gz").exists() for i in args.intervals for k in ("liq", "ohlcv"))
    client, symbols = None, []
    if need_fetch:
        if not key:
            raise SystemExit("Set COINALYZE_API_KEY (free at https://coinalyze.net/account/api-key/)")
        client = Coinalyze(key)
        symbols = btc_perp_symbols(client)
        print(f"{len(symbols)} BTC perpetuals: {', '.join(symbols)}")
    for interval in args.intervals:
        run_interval(client, symbols, interval, args)


if __name__ == "__main__":
    main()
