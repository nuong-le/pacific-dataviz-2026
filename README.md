# Smallest Footprint, Biggest Impact

## Pacific Climate Change — Pacific Dataviz Challenge 2026

The Pacific contributes relatively little to global greenhouse gas emissions, yet Pacific communities face significant and immediate climate risks.

**Smallest Footprint, Biggest Impact** explores how climate-related indicators are changing across the Pacific, how these indicators relate statistically to regional surface temperature anomalies, and what historical trends suggest about possible future trajectories.

The project combines data preparation, statistical analysis, modelling and interactive visual storytelling to turn a complex set of climate indicators into an accessible evidence-based story.

---

## 🌏 Explore the Interactive Visualisation

**[▶ View the Interactive Visualisation](https://nuong-le.github.io/pacific-dataviz-2026/)**

The interactive story brings together long-term temperature and sea-level trends, environmental indicators, statistical relationships, modelled trajectories and contextual evidence about climate risk in the Pacific.

---

# The Story

The project follows a simple analytical journey:

**What is changing? → What moves with temperature? → Which indicators matter statistically? → What could future trajectories look like?**

The analysis begins by constructing regional yearly series from available Pacific reporting data.

It then examines long-term trends and statistical associations between environmental indicators and regional surface temperature anomalies.

A forward-selection model is used to identify which candidate indicators contribute most to explaining variation in the regional temperature series within the available overlapping data.

Finally, linear and quadratic trend models are compared for surface temperature and sea-level anomalies to illustrate possible trajectories towards 2030 and 2050.

The statistical results are then translated into an interactive visual narrative.

---

# Key Findings

## 1. Surface temperature shows a persistent long-term trend

Regional Surface Temperature anomalies are used as the central climate-change reference variable.

A linear ordinary least squares (OLS) trend is fitted against year to examine the direction and strength of the long-term trend.

The analysis reports the estimated slope, R² and statistical significance of the trend.

---

## 2. Climate indicators show different relationships with temperature

Pearson correlation is used to examine statistical associations between regional indicator series and regional Surface Temperature anomalies over their overlapping years.

These relationships help identify patterns that are worth exploring in the climate story.

However, correlation is interpreted as **association, not causation**.

A statistically strong relationship does not by itself demonstrate that one indicator causes changes in temperature.

---

## 3. Forward selection identifies the strongest statistical contributors

A forward-selection procedure starts with an empty model and progressively adds the candidate indicator that provides the greatest improvement in adjusted R² for regional Surface Temperature anomalies.

The procedure continues while the best available addition improves adjusted R² by at least 0.005.

This provides a structured way to identify which indicators contribute most to the statistical model within the available data.

---

## 4. Historical trends suggest continued change, but uncertainty increases

For Surface Temperature anomalies and Sea Level Anomalies, both linear and quadratic models are fitted.

The models are compared using Akaike Information Criterion (AIC).

The resulting models are extrapolated to 2030 and 2050 to illustrate possible trajectories under the historical relationships captured by the models.

These results are **statistical trend projections, not precise climate forecasts**.

They should not be interpreted as physical climate-model predictions or as guaranteed future outcomes.

---

# Data

## Primary Dataset

The core analysis uses the **SPC Climate Change Indicators** dataset provided in:

`Data_CLIMATE_CHANGE.csv`

The dataset contains climate and environmental indicators reported for Pacific Island countries and territories.

The analysis pipeline identifies 13 indicators in the supplied dataset and constructs a regional yearly series for each indicator.

---

## Regional Aggregation

For each indicator, observations are grouped by year and averaged across all territories reporting that indicator in that year.

This produces one regional mean value per year.

The regional mean is therefore an **unweighted mean across available reporting territories**, rather than a population-weighted estimate.

Because reporting coverage can vary across indicators and years, differences in coverage should be considered when interpreting regional trends.

---

# Methodology

## 1. Data Preparation

### `01_clean_data.py`

The raw CSV is loaded and standardised before analysis.

The process:

- selects the required country, indicator, year and observation-value fields;
- removes missing observations;
- standardises country and indicator text;
- identifies the available indicators;
- calculates yearly regional means for each indicator.

The resulting regional time series are saved as:

`regional_series.json`

Each indicator is represented as a series of yearly observations.

---

## 2. Trend and Correlation Analysis

### `02_correlation_analysis.py`

The analysis examines the long-term behaviour of the regional indicators.

For each regional indicator series, the analysis calculates:

- linear OLS trend against year;
- slope;
- R²;
- p-value;
- Pearson correlation with regional Surface Temperature anomalies.

Surface Temperature anomalies are used as the central climate reference variable.

The analysis also performs country-level linear trend analysis for:

- Surface Temperature anomalies;
- Sea Level Anomalies.

This provides additional context for understanding whether regional patterns are also visible across individual reporting territories.

The results are saved as:

`trend_stats.json`

---

## 3. Forward Selection

### `03_forward_selection.py`

Forward selection is used to reduce the set of candidate indicators and identify those that contribute most to the statistical model of regional Surface Temperature anomalies.

The target variable is:

**Surface Temperature anomalies**

The candidate indicators are:

- Sea Level Anomalies
- Greenhouse gaz emission per capita
- Livestock Yield
- Climate Altering Land Cover Index (CALCI)
- Crop Yield
- Precipitation anomalies
- Tourism Arrivals

The procedure:

1. starts with no predictors;
2. evaluates the remaining candidate indicators;
3. identifies the candidate producing the greatest improvement in adjusted R²;
4. adds that candidate to the model;
5. repeats the process;
6. stops when the best remaining candidate improves adjusted R² by less than 0.005.

The analysis uses ordinary least squares implemented with NumPy.

The results are saved as:

`forward_selection.json`

### Candidate exclusions

`Power generation` and `Environmental Taxes` are deliberately excluded
from the candidate set to retain a longer common overlapping data window
for the seven candidate indicators. They could be included in an
alternative model using a shorter, more recent common period.

This is a modelling-scope decision and does not imply that these indicators
are unimportant to climate policy or climate change.

### Model result

The forward-selection procedure identified four indicators in the final
model over the common 1995–2022 period (n = 28).

The final model achieved an adjusted R² of 0.64.

This indicates statistical explanatory power within the observed sample;
it should not be interpreted as evidence of causal relationships.

---

# 4. Trend Model Comparison and Projections

### `04_forecast_models.py`

Two indicators are modelled:

- Surface Temperature anomalies
- Sea Level Anomalies

For each indicator, two polynomial models are fitted:

### Linear model

A first-degree polynomial:

`y = a + bx`

### Quadratic model

A second-degree polynomial:

`y = a + bx + cx²`

The models are compared using Akaike Information Criterion (AIC).

The model with the lower AIC is considered the better in-sample fit.

Both models are extrapolated to:

- 2030
- 2050

The results are saved as:

`model_comparison.json`

### Important interpretation

These projections extend historical statistical relationships beyond the observed period.

They are **not physical climate-model forecasts**.

They do not incorporate:

- future emissions scenarios;
- climate-policy pathways;
- physical climate-system processes;
- future adaptation;
- future technological change;
- changes in reporting behaviour.

Therefore, the 2030 and 2050 values should be interpreted as **trend-based scenarios illustrating possible trajectories**, rather than precise predictions.

---

# 5. Supporting Visual Outputs

### `05_generate_charts.py`

This script generates supporting visualisations using Matplotlib.

It uses the outputs of the analytical pipeline to produce charts for the report/PDF version of the project.

The generated charts include supporting visualisations of:

- regional trends;
- statistical relationships;
- forward-selection results;
- model comparisons;
- projected trajectories.

The charts are saved to:

`OutputChart/`

This step supports the report/PDF visualisation and is separate from the main dashboard data-generation step.

---

# 6. Dashboard Data Preparation

### `06_export_dashboard_json.py`

The statistical outputs are combined into a single:

`data.json`

This file is consumed by the JavaScript used by the interactive HTML dashboard.

The dashboard data package includes:

- regional indicator series;
- trend statistics;
- country-level information;
- forward-selection results;
- model comparison results;
- selected contextual statistics.

This approach allows the browser-based dashboard to present the results without performing the complete statistical analysis in the browser.

---

# Analytical Decisions

Statistical significance alone was not used to determine which findings should appear in the final climate narrative.

The project distinguishes between:

**a statistical pattern**

and

**a pattern that can reasonably support a climate interpretation.**

This distinction is important because an indicator can show a strong statistical trend for reasons unrelated to physical climate change.

For example, indicators affected by changes in monitoring, reporting or administrative capacity may increase over time simply because data collection improves.

The final story therefore combines statistical evidence with contextual interpretation rather than treating every significant trend as a climate signal.

---

# Limitations

The analysis should be interpreted within the limitations of the available data and modelling approach.

### Data limitations

- Regional values are unweighted means across reporting territories.
- Reporting coverage can vary between indicators and years.
- Missing observations can affect comparisons across indicators.
- Differences in data availability may influence the length of each indicator's time series.
- The regional mean does not represent a population-weighted Pacific estimate.

### Statistical limitations

- Pearson correlation measures association, not causation.
- Statistical significance does not establish a causal relationship.
- Forward selection can be sensitive to the candidate variables and available observation period.
- The forward-selection model is based on a relatively limited overlapping sample.
- Model selection using AIC identifies the better in-sample fit but does not guarantee better future performance.

### Projection limitations

- Linear and quadratic models extrapolate historical patterns.
- Uncertainty increases as projections extend further beyond the observed period.
- The models do not reproduce physical climate processes.
- The projections do not incorporate future emissions scenarios or policy pathways.
- The 2030 and 2050 values should therefore be treated as illustrative statistical trajectories rather than precise forecasts.

---

# Reproducible Analysis

The repository contains the source dataset, Python scripts and generated outputs required to inspect and reproduce the core analysis.

## Requirements

Python 3.9+ is recommended.

Install the required packages:

```bash
pip install pandas numpy scipy matplotlib
