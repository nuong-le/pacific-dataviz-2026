"""
01_clean_data.py

Loads the raw SPC Climate Change Indicators CSV, standardises it, and reshapes
each of the 13 indicators into a single "regional series": one value per year,
averaged across every territory that reported that year.

Output: regional_series.json
    { "<indicator name>": [[year, value], [year, value], ...], ... }
"""
import pandas as pd
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent

SRC = ROOT_DIR / "Data_CLIMATE_CHANGE.csv"
OUT = BASE_DIR / "regional_series.json"

COLS = [
    "Pacific Island Countries and territories",
    "Climate Change Indicators",
    "TIME_PERIOD",
    "OBS_VALUE",
]


def load_clean(path: str = SRC) -> pd.DataFrame:
    """Load the raw CSV and keep only the columns needed for analysis."""
    df = pd.read_csv(path)
    df = df[COLS].dropna()
    df.columns = ["country", "indicator", "year", "value"]

    # Standardise country name whitespace/casing quirks (defensive — the source
    # file is fairly clean, but this guards against future data refreshes).
    df["country"] = df["country"].str.strip()
    df["indicator"] = df["indicator"].str.strip()

    return df


def regional_series(df: pd.DataFrame, indicator: str) -> list:
    """Average an indicator across all reporting territories, per year."""
    sub = df[df["indicator"] == indicator]
    agg = sub.groupby("year")["value"].mean().reset_index()
    return [[int(y), round(float(v), 4)] for y, v in zip(agg["year"], agg["value"])]


def main():
    df = load_clean()
    indicators = sorted(df["indicator"].unique())

    print(f"Loaded {len(df):,} rows across {df['country'].nunique()} territories "
          f"and {len(indicators)} indicators.\n")

    series = {}
    for ind in indicators:
        s = regional_series(df, ind)
        years = [p[0] for p in s]
        series[ind] = s
        print(f"{ind:55s} n={len(s):3d}  {min(years)}-{max(years)}")

    with open(OUT, "w") as f:
        json.dump(series, f)
    print(f"\nWrote {OUT}")


if __name__ == "__main__":
    main()
