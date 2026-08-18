"""
05_generate_charts.py

Renders every matplotlib chart used in the PDF/report version of the story,
plus a bar chart of the forward-selection results. Reads from the JSON files
produced by the earlier scripts so it stays in sync with the same numbers
used elsewhere.

Requires: regional_series.json, forward_selection.json, model_comparison.json
Output:   output_charts/*.png
"""
import json
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

OCEAN, DEEP, CORAL = "#0B6E7F", "#0A3D5C", "#E8734A"
TEAL_LIGHT, GREY, GREEN = "#7FB8C4", "#6B7280", "#4C9A6B"
OUT_DIR = "output_charts"

plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 11,
    "axes.edgecolor": "#333333", "axes.labelcolor": "#222222", "text.color": "#222222",
    "xtick.color": "#333333", "ytick.color": "#333333",
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})


def to_df(series):
    return pd.DataFrame(series, columns=["year", "value"])


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    with open("regional_series.json") as f:
        series = json.load(f)
    with open("forward_selection.json") as f:
        fwd = json.load(f)
    with open("model_comparison.json") as f:
        mc = json.load(f)

    temp = to_df(series["Surface Temperature anomalies"])
    sst = to_df(series["Sea Surface Temperature anomalies"])
    sea_level = to_df(series["Sea Level Anomalies"])
    ghg = to_df(series["Greenhouse gaz emission per capita"])
    livestock = to_df(series["Livestock Yield"])
    calci = to_df(series["Climate Altering Land Cover Index (CALCI)"])
    power = to_df(series["Power generation"])
    etax = to_df(series["Environmental Taxes"])

    # country-level sea level, straight from the raw CSV (not in regional_series.json)
    raw = pd.read_csv("Data_CLIMATE_CHANGE.csv")
    raw = raw[["Pacific Island Countries and territories", "Climate Change Indicators",
               "TIME_PERIOD", "OBS_VALUE"]].dropna()
    raw.columns = ["country", "indicator", "year", "value"]
    sl_raw = raw[raw["indicator"] == "Sea Level Anomalies"]

    # ---- 1. Warming ----
    lin = mc["temp"]["linear"]["coefs"]
    x_mean_t = mc["temp"]["x_mean"]
    trend_x = np.array([temp.year.min(), temp.year.max()])
    trend_y = np.polyval(lin, trend_x - x_mean_t)

    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.plot(temp.year, temp.value, color=OCEAN, lw=1.4, alpha=0.85, label="Surface temperature anomaly")
    ax.plot(sst.year, sst.value, color=TEAL_LIGHT, lw=1.2, alpha=0.7, label="Sea surface temperature anomaly")
    ax.plot(trend_x, trend_y, color=CORAL, lw=2.2, ls="--", label="Long-term trend")
    ax.axhline(0, color="#999999", lw=0.8)
    ax.set_title("176 Years of Warming Across the Pacific (1850-2025)", fontsize=14, fontweight="bold", pad=14, loc="left", color=DEEP)
    ax.set_ylabel("Temperature anomaly (°C, vs. baseline)"); ax.set_xlabel("Year")
    ax.legend(frameon=False, loc="upper left")
    r2 = mc["temp"]["linear"]["r2"]
    ax.text(0.99, 0.03, f"R2 = {r2:.2f}  (region-wide mean, n=22 territories)",
            transform=ax.transAxes, ha="right", fontsize=8.5, color=GREY)
    plt.tight_layout(); plt.savefig(f"{OUT_DIR}/01_warming_trend.png", dpi=200); plt.close()

    # ---- 2. Sea level ----
    lin_sl = mc["sea_level"]["linear"]["coefs"]
    x_mean_sl = mc["sea_level"]["x_mean"]
    trend_x2 = np.array([sea_level.year.min(), sea_level.year.max()])
    trend_y2 = np.polyval(lin_sl, trend_x2 - x_mean_sl)

    fig, ax = plt.subplots(figsize=(9.5, 5))
    for c, g in sl_raw.groupby("country"):
        g = g.sort_values("year")
        ax.plot(g.year, g.value, color=TEAL_LIGHT, lw=0.6, alpha=0.35)
    ax.plot(sea_level.year, sea_level.value, color=OCEAN, lw=2.4, label="Regional mean (21 territories)")
    ax.plot(trend_x2, trend_y2, color=CORAL, lw=2.2, ls="--", label="Trend")
    ax.axhline(0, color="#999999", lw=0.8)
    ax.set_title("Sea Level Is Rising Across Every Pacific Territory (1993-2023)", fontsize=14, fontweight="bold", pad=14, loc="left", color=DEEP)
    ax.set_ylabel("Sea level anomaly (m)"); ax.set_xlabel("Year")
    ax.legend(frameon=False, loc="upper left")
    r2sl = mc["sea_level"]["linear"]["r2"]
    ax.text(0.99, 0.03, f"Regional trend R2 = {r2sl:.2f}  |  thin lines = individual territories",
            transform=ax.transAxes, ha="right", fontsize=8.5, color=GREY)
    plt.tight_layout(); plt.savefig(f"{OUT_DIR}/02_sea_level.png", dpi=200); plt.close()

    # ---- 3. Injustice ----
    common = temp[temp.year >= ghg.year.min()]
    fig, ax1 = plt.subplots(figsize=(9.5, 5))
    ax2 = ax1.twinx()
    ax1.plot(common.year, common.value, color=CORAL, lw=2, label="Temperature anomaly (left axis)")
    ax2.plot(ghg.year, ghg.value, color=DEEP, lw=2, label="GHG emissions per capita (right axis)")
    ax1.set_ylabel("Temperature anomaly (°C)", color=CORAL)
    ax2.set_ylabel("GHG emissions per capita (t CO2e)", color=DEEP)
    ax1.tick_params(axis='y', labelcolor=CORAL); ax2.tick_params(axis='y', labelcolor=DEEP)
    ax1.set_xlabel("Year")
    ax1.set_title("Falling Local Emissions, Rising Regional Temperatures", fontsize=14, fontweight="bold", pad=14, loc="left", color=DEEP)
    l1, lb1 = ax1.get_legend_handles_labels(); l2, lb2 = ax2.get_legend_handles_labels()
    ax1.legend(l1+l2, lb1+lb2, frameon=False, loc="upper left")
    plt.tight_layout(); plt.savefig(f"{OUT_DIR}/03_injustice.png", dpi=200); plt.close()

    # ---- 4. Consequences ----
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.6))
    ax = axes[0]; ax2 = ax.twinx()
    t_live = temp[temp.year >= livestock.year.min()]
    ax.plot(t_live.year, t_live.value, color=CORAL, lw=1.6, alpha=0.8)
    ax2.plot(livestock.year, livestock.value, color=GREEN, lw=2)
    ax.set_ylabel("Temp anomaly (°C)", color=CORAL, fontsize=9.5)
    ax2.set_ylabel("Livestock yield (kg/animal)", color=GREEN, fontsize=9.5)
    ax.set_title("Livestock Yield vs. Temperature", fontsize=11.5, fontweight="bold", color=DEEP)

    ax = axes[1]; ax2 = ax.twinx()
    t_calci = temp[temp.year >= calci.year.min()]
    ax.plot(t_calci.year, t_calci.value, color=CORAL, lw=1.6, alpha=0.8)
    ax2.plot(calci.year, calci.value, color=DEEP, lw=2)
    ax.set_ylabel("Temp anomaly (°C)", color=CORAL, fontsize=9.5)
    ax2.set_ylabel("CALCI (%)", color=DEEP, fontsize=9.5)
    ax.set_title("Land Cover Index vs. Temperature", fontsize=11.5, fontweight="bold", color=DEEP)

    fig.suptitle("Warming Is Already Denting Food Security and Land Cover", fontsize=14, fontweight="bold", color=DEEP, x=0.02, ha="left")
    plt.tight_layout(rect=[0, 0, 1, 0.94]); plt.savefig(f"{OUT_DIR}/04_consequences.png", dpi=200); plt.close()

    # ---- 5. Forecast (linear vs quadratic) ----
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.8))
    for ax, df_hist, mc_key, title, ylab, color in [
        (axes[0], temp, "temp", "Temperature Anomaly Forecast", "°C anomaly", CORAL),
        (axes[1], sea_level, "sea_level", "Sea Level Anomaly Forecast", "meters", OCEAN),
    ]:
        m = mc[mc_key]
        x_mean = m["x_mean"]
        ax.plot(df_hist.year, df_hist.value, color=color, lw=1.6, label="Observed")
        future_x = np.array([df_hist.year.max(), 2030, 2050])
        lin_y = np.polyval(m["linear"]["coefs"], future_x - x_mean)
        quad_y = np.polyval(m["quadratic"]["coefs"], future_x - x_mean)
        ax.plot(future_x, lin_y, color="#999999", lw=2, ls="--", label="Linear projection")
        if m["best_model"] == "quadratic":
            ax.plot(future_x, quad_y, color=color, lw=2, ls=":", label="Quadratic projection (better fit)")
        ax.scatter([2030, 2050], lin_y[1:], color=color, zorder=5, s=30)
        ax.set_title(f"{title}\n(best fit: {m['best_model']})", fontsize=11.5, fontweight="bold", color=DEEP)
        ax.set_ylabel(ylab, fontsize=9.5); ax.set_xlabel("Year", fontsize=9)
        ax.legend(frameon=False, fontsize=8, loc="upper left")
    fig.suptitle("Where the Trend Leads: 2030 and 2050 Projections", fontsize=14, fontweight="bold", color=DEEP, x=0.02, ha="left")
    plt.tight_layout(rect=[0, 0, 1, 0.92]); plt.savefig(f"{OUT_DIR}/05_forecast.png", dpi=200); plt.close()

    # ---- 6. Solution ----
    fig, axes = plt.subplots(1, 2, figsize=(9.5, 4.6))
    ax = axes[0]
    ax.plot(power.year, power.value, color=GREEN, lw=2.2, marker='o', markersize=3)
    ax.fill_between(power.year, power.value, color=GREEN, alpha=0.12)
    ax.set_title("Power Generation Is Scaling Up", fontsize=11.5, fontweight="bold", color=DEEP)
    ax.set_ylabel("GWh (regional mean)", fontsize=9.5)

    ax = axes[1]
    ax.plot(etax.year, etax.value, color=DEEP, lw=2.2, marker='o', markersize=3)
    ax.fill_between(etax.year, etax.value, color=DEEP, alpha=0.12)
    ax.set_title("Environmental Taxes Are Rising\n(5 reporting territories)", fontsize=11.5, fontweight="bold", color=DEEP)
    ax.set_ylabel("% (regional mean)", fontsize=9.5)

    fig.suptitle("Signs of an Accelerating Energy & Policy Transition", fontsize=14, fontweight="bold", color=DEEP, x=0.02, ha="left")
    plt.tight_layout(rect=[0, 0, 1, 0.94]); plt.savefig(f"{OUT_DIR}/06_solution.png", dpi=200); plt.close()

    # ---- 7. Forward selection scree chart ----
    hist = fwd["history"]
    fig, ax = plt.subplots(figsize=(8, 4))
    steps = [h["step"] for h in hist]
    labels = [h["feature"] for h in hist]
    adj_r2 = [h["adj_r2"] for h in hist]
    ax.barh(range(len(hist)), adj_r2, color=OCEAN)
    ax.set_yticks(range(len(hist))); ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.set_xlabel("Adjusted R2 after adding this feature")
    ax.set_title(f"Forward Selection: Predicting Temperature Anomaly (n={fwd['n_obs']})", fontsize=12, fontweight="bold", color=DEEP, loc="left", wrap=True)
    for i, v in enumerate(adj_r2):
        ax.text(v + 0.01, i, f"{v:.2f}", va="center", fontsize=9, color=GREY)
    plt.tight_layout(); plt.savefig(f"{OUT_DIR}/07_forward_selection.png", dpi=200); plt.close()

    print(f"All charts written to {OUT_DIR}/")


if __name__ == "__main__":
    main()
