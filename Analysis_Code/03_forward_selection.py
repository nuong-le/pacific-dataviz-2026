"""
03_forward_selection.py

Dimensionality reduction via forward (stepwise) selection: starting from an
empty model, repeatedly add whichever candidate indicator most improves
adjusted R-squared for predicting regional Surface Temperature anomaly, and
stop once the best remaining addition gains less than a small threshold.

This is deliberately implemented with plain numpy least-squares (no
statsmodels/sklearn dependency) so it runs anywhere Python + numpy + scipy
are available.

Requires: regional_series.json (output of 01_clean_data.py)
Output:   forward_selection.json
"""
import json
import numpy as np
import pandas as pd
from scipy import stats

TARGET = "Surface Temperature anomalies"

# Candidate predictors. Power generation and Environmental Taxes are excluded
# here to keep a longer overlapping year window (see README) — feel free to
# add them back in if you want a shorter, more recent panel instead.
CANDIDATES = [
    "Sea Level Anomalies",
    "Greenhouse gaz emission per capita",
    "Livestock Yield",
    "Climate Altering Land Cover Index (CALCI)",
    "Crop Yield",
    "Precipitation anomalies",
    "Tourism Arrivals",
]

IMPROVEMENT_THRESHOLD = 0.005  # minimum adjusted-R2 gain to keep adding features


def ols_r2(X: np.ndarray, y: np.ndarray):
    """Fit y ~ X (+ intercept) via least squares; return R2, adjusted R2, model p-value."""
    n = len(y)
    Xc = np.column_stack([np.ones(n), X])
    coef, *_ = np.linalg.lstsq(Xc, y, rcond=None)
    resid = y - Xc @ coef
    ss_res = np.sum(resid ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    k = Xc.shape[1] - 1
    adj_r2 = 1 - (1 - r2) * (n - 1) / (n - k - 1) if n - k - 1 > 0 else np.nan
    if k > 0 and ss_res > 0:
        f_stat = ((ss_tot - ss_res) / k) / (ss_res / (n - k - 1))
        p_val = 1 - stats.f.cdf(f_stat, k, n - k - 1)
    else:
        p_val = np.nan
    return r2, adj_r2, p_val


def forward_select(merged: pd.DataFrame, candidates: list, target_col: str = "target"):
    y = merged[target_col].values
    remaining = list(candidates)
    selected, history = [], []
    current_adj_r2 = 0.0

    while remaining:
        scored = []
        for feat in remaining:
            X = merged[selected + [feat]].values
            r2, adj_r2, p = ols_r2(X, y)
            scored.append((adj_r2, feat, r2, p))
        scored.sort(reverse=True, key=lambda t: t[0])
        best_adj_r2, best_feat, best_r2, best_p = scored[0]

        if best_adj_r2 > current_adj_r2 + IMPROVEMENT_THRESHOLD:
            selected.append(best_feat)
            remaining.remove(best_feat)
            current_adj_r2 = best_adj_r2
            history.append({
                "step": len(selected), "feature": best_feat,
                "r2": round(float(best_r2), 4), "adj_r2": round(float(best_adj_r2), 4),
                "model_p": float(best_p),
            })
        else:
            break
    return selected, history


def main():
    with open("regional_series.json") as f:
        series = json.load(f)

    target = pd.DataFrame(series[TARGET], columns=["year", "target"]).set_index("year")
    merged = target.copy()
    for c in CANDIDATES:
        s = pd.DataFrame(series[c], columns=["year", c]).set_index("year")
        merged = merged.join(s, how="inner")
    merged = merged.dropna()

    print(f"Overlapping year window: {merged.index.min()}-{merged.index.max()} "
          f"(n={len(merged)} years)\n")

    selected, history = forward_select(merged, CANDIDATES)

    print("Forward selection order:")
    for h in history:
        print(f"  step {h['step']}: +{h['feature']:35s} "
              f"R2={h['r2']:.3f}  adj_R2={h['adj_r2']:.3f}  model p={h['model_p']:.2e}")

    out = {
        "target": TARGET,
        "candidates": CANDIDATES,
        "common_years": [int(merged.index.min()), int(merged.index.max())],
        "n_obs": int(len(merged)),
        "selected_features": selected,
        "history": history,
    }
    with open("forward_selection.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nWrote forward_selection.json")


if __name__ == "__main__":
    main()
