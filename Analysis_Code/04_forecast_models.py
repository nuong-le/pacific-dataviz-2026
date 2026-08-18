"""
04_forecast_models.py

For Temperature and Sea Level, fits both a linear (degree-1) and quadratic
(degree-2) polynomial against year, compares them via AIC, and forecasts
2030 / 2050 under both models.

Requires: regional_series.json (output of 01_clean_data.py)
Output:   model_comparison.json
"""
import json
import numpy as np

INDICATORS = {
    "temp": "Surface Temperature anomalies",
    "sea_level": "Sea Level Anomalies",
}
FORECAST_YEARS = [2030, 2050]


def aic(n: int, ss_res: float, k: int) -> float:
    """Akaike Information Criterion for a least-squares fit (Gaussian errors)."""
    return n * np.log(ss_res / n) + 2 * k


def fit_poly(x: np.ndarray, y: np.ndarray, degree: int):
    coefs = np.polyfit(x, y, degree)
    yhat = np.polyval(coefs, x)
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    k = degree + 2  # number of fitted parameters (coeffs + noise variance)
    return coefs, r2, aic(len(y), ss_res, k)


def main():
    with open("regional_series.json") as f:
        series = json.load(f)

    results = {}
    for name, indicator in INDICATORS.items():
        arr = np.array(series[indicator])
        x_raw, y = arr[:, 0], arr[:, 1]
        x_mean = x_raw.mean()
        x = x_raw - x_mean  # centre for numerical stability

        lin_coefs, lin_r2, lin_aic = fit_poly(x, y, 1)
        quad_coefs, quad_r2, quad_aic = fit_poly(x, y, 2)
        best = "linear" if lin_aic <= quad_aic else "quadratic"

        print(f"--- {indicator} ---")
        print(f"  Linear:    R2={lin_r2:.4f}  AIC={lin_aic:8.2f}")
        print(f"  Quadratic: R2={quad_r2:.4f}  AIC={quad_aic:8.2f}")
        print(f"  Better fit by AIC: {best}")

        forecasts = {}
        for yr in FORECAST_YEARS:
            xv = yr - x_mean
            lin_pred = float(np.polyval(lin_coefs, xv))
            quad_pred = float(np.polyval(quad_coefs, xv))
            forecasts[yr] = {"linear": round(lin_pred, 3), "quadratic": round(quad_pred, 3)}
            print(f"  {yr}: linear={lin_pred:+.3f}  quadratic={quad_pred:+.3f}")
        print()

        results[name] = {
            "indicator": indicator,
            "x_mean": float(x_mean),
            "linear": {"coefs": lin_coefs.tolist(), "r2": round(float(lin_r2), 4), "aic": round(float(lin_aic), 2)},
            "quadratic": {"coefs": quad_coefs.tolist(), "r2": round(float(quad_r2), 4), "aic": round(float(quad_aic), 2)},
            "best_model": best,
            "forecasts": forecasts,
        }

    with open("model_comparison.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Wrote model_comparison.json")


if __name__ == "__main__":
    main()
