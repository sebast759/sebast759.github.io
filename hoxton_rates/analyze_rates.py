"""
Analyze nightly rates for The Hoxton, Shepherd's Bush and rank demand signals.

Input : hoxton_shepherds_bush_daily_rates.csv
Output: hoxton_price_anomalies.csv, hoxton_demand_report.md

Rules:
  * Missing observations stay missing. No interpolation, no forward fill.
    A missing night is excluded from medians and breaks clusters and jump comparisons.
  * Sold out nights have no price but are treated as the strongest demand signal.
  * Primary price = price_gbp (cheapest available standard rate, refundable or not).

Usage:
  python analyze_rates.py [--input PATH] [--outdir DIR]
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

START = "2026-10-08"
END = "2027-04-07"

ROLL_WINDOW = 28
ROLL_MIN_PERIODS = 14
EXPENSIVE_PREM = 0.20      # premium vs weekday or rolling median that marks a night as expensive
WEEKEND_PREM = 0.15        # Fri/Sat premium vs own weekday median that flags a weekend
JUMP_THRESHOLD = 0.20      # price vs mean of observed adjacent nights
LIST_PREM = 0.10           # minimum premium to appear in the anomalies file without another flag

W_WD, W_ROLL, W_JUMP = 0.45, 0.35, 0.20
CLUSTER_BONUS_PER_NIGHT, CLUSTER_BONUS_CAP = 0.25, 1.0


def robust_z(s: pd.Series) -> pd.Series:
    med = s.median()
    mad = (s - med).abs().median() * 1.4826
    if not np.isfinite(mad) or mad == 0:
        sd = s.std()
        mad = sd if np.isfinite(sd) and sd > 0 else 1.0
    return (s - med) / mad


def to_bool(s: pd.Series) -> pd.Series:
    return s.astype("string").str.strip().str.lower().isin(["true", "1", "yes", "y"])


def load(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"]).dt.normalize()
    df["price_gbp"] = pd.to_numeric(df["price_gbp"], errors="coerce")
    df["refundable_price_gbp"] = pd.to_numeric(df["refundable_price_gbp"], errors="coerce")
    df["taxes_gbp"] = pd.to_numeric(df["taxes_gbp"], errors="coerce")
    df["sold_out"] = to_bool(df["sold_out"])
    df["promotion"] = df["promotion"].astype("string")
    if df["date"].duplicated().any():
        dups = df.loc[df["date"].duplicated(keep=False), "date"].dt.date.unique()
        raise ValueError(f"Duplicate dates in input: {list(dups)}")

    # Reindex on the full calendar so absent dates are explicit gaps, never filled.
    cal = pd.DataFrame({"date": pd.date_range(START, END, freq="D")})
    df = cal.merge(df, on="date", how="left")
    df["day_of_week"] = df["date"].dt.day_name()
    df["sold_out"] = df["sold_out"].astype("boolean").fillna(False).astype(bool)
    df["status"] = np.where(
        df["sold_out"], "sold_out", np.where(df["price_gbp"].notna(), "observed", "missing")
    )
    return df.set_index("date")


def compute(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    p = df["price_gbp"].where(~df["sold_out"])

    # 1. Weekday medians and 2. premium vs weekday median
    wd_med = p.groupby(df["day_of_week"]).median()
    df["weekday_median"] = df["day_of_week"].map(wd_med)
    df["prem_vs_weekday"] = p / df["weekday_median"] - 1

    # 3. Rolling 28 day median (centered, calendar based, gaps stay NaN) and 4. premium vs it
    df["rolling_28d_median"] = p.rolling(ROLL_WINDOW, center=True, min_periods=ROLL_MIN_PERIODS).median()
    df["prem_vs_rolling"] = p / df["rolling_28d_median"] - 1

    # 5. Percentiles
    q75, q90, q95 = p.quantile([0.75, 0.90, 0.95]).tolist()
    df["price_percentile"] = p.rank(pct=True)
    df["above_p75"] = p > q75
    df["above_p90"] = p > q90
    df["above_p95"] = p > q95

    # 8. Jumps vs observed adjacent calendar nights (no bridging over gaps)
    prev_p, next_p = p.shift(1), p.shift(-1)
    adj_mean = pd.concat([prev_p, next_p], axis=1).mean(axis=1, skipna=True)
    df["prev_night_gbp"] = prev_p
    df["next_night_gbp"] = next_p
    df["jump_vs_adjacent"] = p / adj_mean - 1
    df["jump_flag"] = df["jump_vs_adjacent"] >= JUMP_THRESHOLD

    # 6. Clusters of consecutive expensive nights (sold out counts as expensive, missing breaks a run)
    expensive = (
        (df["prem_vs_weekday"] >= EXPENSIVE_PREM)
        | (df["prem_vs_rolling"] >= EXPENSIVE_PREM)
        | df["above_p90"]
        | df["sold_out"]
    ).fillna(False)
    run_id = (expensive != expensive.shift()).cumsum()
    run_len = expensive.groupby(run_id).transform("size")
    in_cluster = expensive & (run_len >= 2)
    cluster_codes = run_id.where(in_cluster)
    mapping = {rid: i + 1 for i, rid in enumerate(pd.unique(cluster_codes.dropna()))}
    df["cluster_id"] = cluster_codes.map(mapping).astype("Int64")
    df["cluster_len"] = run_len.where(in_cluster).astype("Int64")

    # 7. Weekends with unusually high Friday or Saturday pricing
    is_fri_sat = df["day_of_week"].isin(["Friday", "Saturday"])
    df["weekend_flag"] = (is_fri_sat & ((df["prem_vs_weekday"] >= WEEKEND_PREM) | df["sold_out"])).fillna(False)

    # Composite demand score
    z_wd = robust_z(df["prem_vs_weekday"])
    z_roll = robust_z(df["prem_vs_rolling"])
    z_jump = robust_z(df["jump_vs_adjacent"]).clip(lower=0)
    score = W_WD * z_wd.fillna(0) + W_ROLL * z_roll.fillna(0) + W_JUMP * z_jump.fillna(0)
    bonus = ((df["cluster_len"].astype("float") - 1) * CLUSTER_BONUS_PER_NIGHT).clip(upper=CLUSTER_BONUS_CAP).fillna(0)
    score = score + bonus
    score = score.where(df["status"] != "missing")
    sold_out_score = (score.max() if score.notna().any() else 0) + 1
    df["demand_score"] = score.mask(df["sold_out"], sold_out_score)

    def signals(r) -> str:
        out = []
        if r.sold_out:
            out.append("sold_out")
        if r.above_p95:
            out.append("p95")
        elif r.above_p90:
            out.append("p90")
        elif r.above_p75:
            out.append("p75")
        if pd.notna(r.prem_vs_weekday) and r.prem_vs_weekday >= EXPENSIVE_PREM:
            out.append(f"weekday+{r.prem_vs_weekday:.0%}")
        if pd.notna(r.prem_vs_rolling) and r.prem_vs_rolling >= EXPENSIVE_PREM:
            out.append(f"rolling+{r.prem_vs_rolling:.0%}")
        if r.jump_flag is True:
            out.append(f"jump+{r.jump_vs_adjacent:.0%}")
        if pd.notna(r.cluster_id):
            out.append(f"cluster#{r.cluster_id}({r.cluster_len}n)")
        if r.weekend_flag:
            out.append("hot_weekend")
        return ";".join(out)

    df["jump_flag"] = df["jump_flag"].fillna(False)
    for c in ["above_p75", "above_p90", "above_p95"]:
        df[c] = df[c].fillna(False)
    df["signals"] = [signals(r) for r in df.itertuples()]

    listed = (
        df["sold_out"]
        | df["above_p75"]
        | df["jump_flag"]
        | df["weekend_flag"]
        | df["cluster_id"].notna()
        | (df["prem_vs_weekday"] >= LIST_PREM).fillna(False)
        | (df["prem_vs_rolling"] >= LIST_PREM).fillna(False)
    )
    anomalies = df[listed].sort_values("demand_score", ascending=False).reset_index()
    anomalies.insert(0, "rank", range(1, len(anomalies) + 1))
    anomalies["date"] = anomalies["date"].dt.date

    clusters = (
        df[df["cluster_id"].notna()]
        .reset_index()
        .groupby("cluster_id")
        .agg(
            start=("date", "min"),
            end=("date", "max"),
            nights=("date", "size"),
            sold_out_nights=("sold_out", "sum"),
            mean_price=("price_gbp", "mean"),
            mean_prem_wd=("prem_vs_weekday", "mean"),
            mean_score=("demand_score", "mean"),
        )
        .sort_values("mean_score", ascending=False)
    )

    weekday_table = pd.DataFrame(
        {
            "median_gbp": wd_med,
            "observed_nights": p.groupby(df["day_of_week"]).count(),
        }
    ).reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

    df.attrs["quantiles"] = (q75, q90, q95)
    return anomalies, clusters, weekday_table


def fmt_pct(x) -> str:
    return "" if pd.isna(x) else f"{x:+.0%}"


def fmt_gbp(x) -> str:
    return "" if pd.isna(x) else f"£{x:,.0f}"


def md_table(frame: pd.DataFrame) -> str:
    cols = list(frame.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join(["---"] * len(cols)) + "|"]
    for _, r in frame.iterrows():
        lines.append("| " + " | ".join(str(v) for v in r.values) + " |")
    return "\n".join(lines)


def build_report(df, anomalies, clusters, weekday_table) -> str:
    q75, q90, q95 = df.attrs["quantiles"]
    n_total = len(df)
    n_obs = int((df["status"] == "observed").sum())
    n_sold = int((df["status"] == "sold_out").sum())
    n_miss = int((df["status"] == "missing").sum())
    sources = df["source"].dropna().value_counts()
    ts = df["scrape_timestamp"].dropna()
    promo = df["promotion"].dropna()
    promo = promo[~promo.str.lower().isin(["", "none", "false", "no"])]

    out = ["# Hoxton Shepherd's Bush: demand signals for Airbnb pricing", ""]
    out += ["## Data coverage", ""]
    out += [
        f"* Calendar nights: {n_total} ({START} to {END})",
        f"* Priced: {n_obs} | Sold out: {n_sold} | Missing (not filled): {n_miss}",
        f"* Sources: " + (", ".join(f"{k} ({v})" for k, v in sources.items()) or "none"),
        f"* Scrape window: {ts.min()} to {ts.max()}" if len(ts) else "* Scrape window: unknown",
        f"* Nights with a promotion or member rate shown: {len(promo)}",
        f"* Price percentiles: p75 {fmt_gbp(q75)}, p90 {fmt_gbp(q90)}, p95 {fmt_gbp(q95)}",
        "",
    ]

    out += ["## Weekday medians", ""]
    wt = weekday_table.reset_index().rename(columns={"index": "day", "day_of_week": "day"})
    wt["median_gbp"] = wt["median_gbp"].map(fmt_gbp)
    out += [md_table(wt), ""]

    out += ["## Strongest single nights (top 15)", ""]
    top = anomalies.head(15).copy()
    top = pd.DataFrame(
        {
            "rank": top["rank"],
            "date": top["date"],
            "day": top["day_of_week"].str[:3],
            "price": top["price_gbp"].map(fmt_gbp),
            "vs weekday": top["prem_vs_weekday"].map(fmt_pct),
            "vs 28d": top["prem_vs_rolling"].map(fmt_pct),
            "signals": top["signals"],
        }
    )
    out += [md_table(top) if len(top) else "No flagged nights.", ""]

    out += ["## Expensive clusters (2+ consecutive nights)", ""]
    if len(clusters):
        c = clusters.reset_index().copy()
        c = pd.DataFrame(
            {
                "cluster": c["cluster_id"],
                "start": c["start"].dt.date,
                "end": c["end"].dt.date,
                "nights": c["nights"],
                "sold out": c["sold_out_nights"],
                "mean price": c["mean_price"].map(fmt_gbp),
                "mean vs weekday": c["mean_prem_wd"].map(fmt_pct),
            }
        )
        out += [md_table(c), ""]
    else:
        out += ["None found.", ""]

    out += ["## Hot weekends (Fri or Sat premium >= " + f"{WEEKEND_PREM:.0%} or sold out)", ""]
    wk = df[df["weekend_flag"]].reset_index()
    if len(wk):
        wk = pd.DataFrame(
            {
                "date": wk["date"].dt.date,
                "day": wk["day_of_week"].str[:3],
                "price": wk["price_gbp"].map(fmt_gbp),
                "vs weekday": wk["prem_vs_weekday"].map(fmt_pct),
                "sold out": wk["sold_out"],
            }
        )
        out += [md_table(wk), ""]
    else:
        out += ["None found.", ""]

    out += ["## Sudden jumps vs adjacent nights (>= " + f"{JUMP_THRESHOLD:.0%})", ""]
    jp = df[df["jump_flag"]].reset_index()
    if len(jp):
        jp = pd.DataFrame(
            {
                "date": jp["date"].dt.date,
                "day": jp["day_of_week"].str[:3],
                "prev": jp["prev_night_gbp"].map(fmt_gbp),
                "price": jp["price_gbp"].map(fmt_gbp),
                "next": jp["next_night_gbp"].map(fmt_gbp),
                "jump": jp["jump_vs_adjacent"].map(fmt_pct),
            }
        )
        out += [md_table(jp), ""]
    else:
        out += ["None found.", ""]

    if n_miss:
        miss = df.index[df["status"] == "missing"].strftime("%Y-%m-%d").tolist()
        out += ["## Missing nights (excluded, not filled)", "", ", ".join(miss), ""]

    out += [
        "## Caveats",
        "",
        "* Single snapshot: near dates are observed at short lead time, far dates at up to 6 months. "
        "Hotel revenue management raises or lowers rates as dates approach, so far out premiums are weaker evidence. "
        "Re-scrape weekly and compare to separate lead time effects from true demand.",
        "* Cheapest rate is often non refundable; refundable spread is in the input CSV but not used for scoring.",
        "* Member or promo rates can depress observed prices on specific nights; check the promotion column before acting.",
        "* One hotel is a proxy for local demand. Confirm with event calendars (Olympia, Shepherd's Bush Empire, "
        "Loftus Road, BBC/White City) and Airbnb comp set occupancy before raising prices.",
        "* This report recommends where to look. No Airbnb prices were changed.",
        "",
    ]
    return "\n".join(out)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", default="hoxton_shepherds_bush_daily_rates.csv")
    ap.add_argument("--outdir", default=".")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    df = load(Path(args.input))
    anomalies, clusters, weekday_table = compute(df)

    cols = [
        "rank", "date", "day_of_week", "demand_score", "signals", "price_gbp", "refundable_price_gbp",
        "room_type", "promotion", "sold_out", "weekday_median", "prem_vs_weekday", "rolling_28d_median",
        "prem_vs_rolling", "price_percentile", "above_p75", "above_p90", "above_p95", "prev_night_gbp",
        "next_night_gbp", "jump_vs_adjacent", "jump_flag", "cluster_id", "cluster_len", "weekend_flag", "source",
    ]
    anomalies[cols].round(4).to_csv(outdir / "hoxton_price_anomalies.csv", index=False)
    (outdir / "hoxton_demand_report.md").write_text(build_report(df, anomalies, clusters, weekday_table))
    print(f"anomalies: {len(anomalies)} rows, clusters: {len(clusters)}")


if __name__ == "__main__":
    main()
