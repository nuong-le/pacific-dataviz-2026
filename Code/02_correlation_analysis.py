"""
02_correlation_analysis.py

For every indicator's regional series:
  1. Fits an OLS linear trend against year (slope, R², p-value)
  2. Computes the Pearson correlation with regional Surface Temperature anomaly
     (the "climate change" reference variable used throughout the story)

Also runs country-level trend regressions for Temperature and Sea Level, to
confirm the regional pattern holds for individual territories, not just in
aggregate.

Requires: regional_series.json (output of 01_clean_data.py)
Output:   trend_stats.json
"""
import json
import numpy as np
from scipy import stats
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

TARGET_INDICATOR = "Surface Temperature anomalies"


def linear_trend(series: list) -> dict:
    """OLS regression of value against year. series = [[year, value], ...]"""
    arr = np.array(series)
    x, y = arr[:, 0], arr[:, 1]
    slope, intercept, r, p, se = stats.linregress(x, y)
    return {
        "slope": slope, "intercept": intercept, "r2": r ** 2, "p": p,
        "min_year": int(x.min()), "max_year": int(x.max()), "n": len(x),
    }


def correlation_with_target(series: list, target: dict) -> dict:
    """Pearson correlation between an indicator and the target, on overlapping years."""
    s_df = pd.DataFrame(series, columns=["year", "value"])
    t_df = pd.DataFrame(target, columns=["year", "t_value"])
    merged = s_df.merge(t_df, on="year").dropna()
    if len(merged) < 5:
        return {"r": None, "p": None, "n": len(merged)}
    r, p = stats.pearsonr(merged["value"], merged["t_value"])
    return {"r": round(float(r), 3), "p": float(p), "n": len(merged)}


def country_level_trends(csv_path: str, indicator: str) -> list:
    """Run the same linear trend per territory (not the regional mean)."""
    df = pd.read_csv(csv_path)
    df = df[["Pacific Island Countries and territories", "Climate Change Indicators",
              "TIME_PERIOD", "OBS_VALUE"]].dropna()
    df.columns = ["country", "indicator", "year", "value"]
    sub = df[df["indicator"] == indicator]

    results = []
    for country, g in sub.groupby("country"):
        g = g.sort_values("year")
        if len(g) < 5:
            continue
        slope, intercept, r, p, se = stats.linregress(g["year"], g["value"])
        results.append({"country": country, "slope": round(float(slope), 5),
                         "r2": round(float(r ** 2), 3), "p": float(p), "n": len(g)})
    return sorted(results, key=lambda d: -d["slope"])


def main():
    with open(BASE_DIR / "regional_series.json") as f:
        series = json.load(f)

    target = series[TARGET_INDICATOR]

    print("=== Regional linear trend (value ~ year) ===\n")
    trends = {}
    for indicator, s in series.items():
        t = linear_trend(s)
        trends[indicator] = t
        sig = "***" if t["p"] < 0.001 else ("**" if t["p"] < 0.01 else ("*" if t["p"] < 0.05 else ""))
        print(f"{indicator:55s} R2={t['r2']:.3f}  p={t['p']:.2e} {sig}")

    print(f"\n=== Correlation with {TARGET_INDICATOR} ===\n")
    correlations = {}
    for indicator, s in series.items():
        if indicator == TARGET_INDICATOR:
            continue
        c = correlation_with_target(s, target)
        correlations[indicator] = c
        if c["r"] is not None:
            print(f"{indicator:55s} r={c['r']:+.3f}  p={c['p']:.2e}  n={c['n']}")

    print("\n=== Country-level trends: Surface Temperature anomalies ===")
    country_temp = country_level_trends(ROOT_DIR / "Data_CLIMATE_CHANGE.csv", "Surface Temperature anomalies")
    n_sig = sum(1 for c in country_temp if c["p"] < 0.05)
    print(f"{n_sig}/{len(country_temp)} territories individually significant (p<0.05)")

    print("\n=== Country-level trends: Sea Level Anomalies ===")
    country_sl = country_level_trends(ROOT_DIR / "Data_CLIMATE_CHANGE.csv", "Sea Level Anomalies")
    n_sig_sl = sum(1 for c in country_sl if c["p"] < 0.05)
    print(f"{n_sig_sl}/{len(country_sl)} territories individually significant (p<0.05)")

    out = {
        "trends": trends,
        "correlations_vs_temp": correlations,
        "country_temp_trends": country_temp,
        "country_sea_level_trends": country_sl,
    }
    with open(BASE_DIR / "trend_stats.json", "w") as f:
        json.dump(out, f, indent=2, default=float)
    print("\nWrote trend_stats.json")


if __name__ == "__main__":
    main()
