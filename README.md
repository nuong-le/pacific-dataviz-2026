# Pacific Climate Change — Analysis Code

Python 3 scripts that reproduce every number, chart, and statistical result used in the
infographic ("Smallest Footprint, Biggest Impact"). Run them in order — each one writes
its output to disk so later scripts (and the HTML dashboard) can reuse it.

## Why Python

Everything here is standard pandas/numpy/scipy/matplotlib — no proprietary software,
no notebooks required (though it'll run fine in one). It's the most reproducible option:
anyone with Python 3.9+ can `pip install` the four packages below and re-run the whole
analysis end to end, or swap in updated source data and get updated results automatically.

## Setup

```bash
pip install pandas numpy scipy matplotlib
```

## Folder contents

| File | What it does | Output |
|---|---|---|
| `Data_CLIMATE_CHANGE.csv` | Source dataset (SPC Climate Change Indicators) | — |
| `01_clean_data.py` | Loads the raw CSV, standardises it, builds one regional (all-territory-mean) yearly series per indicator | `regional_series.json` |
| `02_correlation_analysis.py` | Linear trend (OLS vs. year) and Pearson correlation for every indicator | prints table + `trend_stats.json` |
| `03_forward_selection.py` | Stepwise forward selection — which indicators best explain regional temperature anomaly | prints step-by-step results + `forward_selection.json` |
| `04_forecast_models.py` | Compares linear vs. quadratic (2nd-degree polynomial) fits per indicator via AIC, forecasts 2030 / 2050 | prints comparison + `model_comparison.json` |
| `05_generate_charts.py` | Renders all matplotlib chart PNGs used in the PDF report | `output_charts/*.png` |
| `06_export_dashboard_json.py` | Packages everything above into the single `data.json` consumed by the HTML dashboard's JavaScript | `data.json` |

## Run everything

```bash
python3 01_clean_data.py
python3 02_correlation_analysis.py
python3 03_forward_selection.py
python3 04_forecast_models.py
python3 05_generate_charts.py
python3 06_export_dashboard_json.py
```

## Method notes

- **Regional series**: each indicator is averaged across all reporting territories per
  year — this is the "regional mean" used throughout the story.
- **Forward selection**: starts with zero predictors, adds whichever remaining indicator
  most improves adjusted R² against regional temperature anomaly, stops once the next-best
  addition gains less than 0.005. Run on the 1995–2022 window where 7 candidate indicators
  overlap (n=28 years).
- **Model comparison**: for temperature and sea level, a linear (degree-1) and quadratic
  (degree-2) polynomial are both fit; the one with the lower AIC is treated as the better
  in-sample fit. Forecasts show both, since higher-degree curves get less reliable the
  further they're extrapolated beyond the observed data.
- **Excluded on purpose**: Meteorological Monitoring Network and Fisheries Management
  Measures both have very low p-values but were excluded from the climate narrative —
  their trend reflects growth in reporting infrastructure over time, not a climate signal.
