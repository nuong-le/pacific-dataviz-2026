"""
06_export_dashboard_json.py

Combines the outputs of every earlier script into the single data.json that
the HTML dashboard's JavaScript reads to draw its charts and stats. Run this
last, after 01-04 (05 is independent — it only makes PNGs for the PDF).

Requires: regional_series.json, trend_stats.json, forward_selection.json,
          model_comparison.json
Output:   data.json
"""
import json
import pandas as pd

INDICATOR_KEY_MAP = {
    "temp": "Surface Temperature anomalies",
    "sst": "Sea Surface Temperature anomalies",
    "sea_level": "Sea Level Anomalies",
    "ghg": "Greenhouse gaz emission per capita",
    "livestock": "Livestock Yield",
    "calci": "Climate Altering Land Cover Index (CALCI)",
    "power": "Power generation",
    "etax": "Environmental Taxes",
    "crop": "Crop Yield",
}


def main():
    with open("regional_series.json") as f:
        series = json.load(f)
    with open("trend_stats.json") as f:
        trend_stats = json.load(f)
    with open("forward_selection.json") as f:
        fwd = json.load(f)
    with open("model_comparison.json") as f:
        mc = json.load(f)

    data = {short: series[full] for short, full in INDICATOR_KEY_MAP.items()}

    data["trends"] = {
        "temp": trend_stats["trends"]["Surface Temperature anomalies"],
        "sea_level": trend_stats["trends"]["Sea Level Anomalies"],
        "power": trend_stats["trends"]["Power generation"],
    }

    data["country_sea_level"] = [
        {"country": c["country"], "slope": c["slope"], "latest": None}
        for c in trend_stats["country_sea_level_trends"]
    ]

    # per-country sea level series, straight from the raw CSV
    raw = pd.read_csv("Data_CLIMATE_CHANGE.csv")
    raw = raw[["Pacific Island Countries and territories", "Climate Change Indicators",
               "TIME_PERIOD", "OBS_VALUE"]].dropna()
    raw.columns = ["country", "indicator", "year", "value"]
    sl = raw[raw["indicator"] == "Sea Level Anomalies"]
    country_series = {}
    for c, g in sl.groupby("country"):
        g = g.sort_values("year")
        if len(g) < 5:
            continue
        country_series[c] = [[int(y), round(float(v), 4)] for y, v in zip(g.year, g.value)]
    data["country_sea_level_series"] = country_series

    data["forward_selection"] = fwd
    data["model_comparison"] = {
        "temp": {
            "x_mean": mc["temp"]["x_mean"],
            "lin_coefs": mc["temp"]["linear"]["coefs"],
            "lin_r2": mc["temp"]["linear"]["r2"],
            "poly_coefs": mc["temp"]["quadratic"]["coefs"],
            "poly_r2": mc["temp"]["quadratic"]["r2"],
            "best_model": mc["temp"]["best_model"],
        },
        "sea_level": {
            "x_mean": mc["sea_level"]["x_mean"],
            "lin_coefs": mc["sea_level"]["linear"]["coefs"],
            "lin_r2": mc["sea_level"]["linear"]["r2"],
            "poly_coefs": mc["sea_level"]["quadratic"]["coefs"],
            "poly_r2": mc["sea_level"]["quadratic"]["r2"],
            "best_model": mc["sea_level"]["best_model"],
        },
    }

    # Real-world context stats used in the "Right Now" section — sourced
    # separately (see README / HTML footer references), hardcoded here since
    # they don't come from the SPC dataset.
    data["context"] = {
        "typhoon2025": {"storms": 27, "typhoons": 13, "fatalities": 653, "damage_usd_b": 10.8},
        "spc_cyclone_2025_26": {"cyclones": 2, "note": "record-low South Pacific season, tied with 1990-91"},
        "sids_exposure_pct": 30,
        "pic_emission_share_pct": 0.1,
    }

    with open("data.json", "w") as f:
        json.dump(data, f)
    print(f"Wrote data.json ({len(json.dumps(data))/1024:.1f} KB) — ready for the HTML dashboard.")


if __name__ == "__main__":
    main()
