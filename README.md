# Smallest Footprint, Biggest Impact

## Pacific Climate Change — Data Visualisation Project

The Pacific contributes relatively little to global greenhouse gas emissions, yet Pacific communities face some of the world's most immediate climate risks.

**Smallest Footprint, Biggest Impact** explores how climate-related indicators have changed across the Pacific, how these changes relate to regional temperature anomalies, and what historical trends suggest about possible future trajectories.

The project combines data analysis, statistical modelling and interactive visual storytelling to turn a complex set of climate indicators into an accessible evidence-based story.

---

## 🌏 Explore the interactive visualisation

**[▶ View the interactive dashboard](YOUR-GITHUB-PAGES-URL)**

The interactive visualisation presents the main story through long-term climate trends, regional patterns, statistical relationships and modelled projections.

---

## The story

The analysis follows a simple journey:

**Observed change → Regional patterns → Statistical relationships → Modelled trajectories → Why this matters**

Rather than treating every statistically significant indicator as evidence of climate change, the analysis applies statistical checks and analytical judgement to identify patterns that are most relevant to the climate story.

---

## Key findings

The analysis highlights several important patterns across the available Pacific climate indicators:

### 1. Long-term warming

Regional temperature anomaly shows a persistent long-term change over the observed period, providing the wider climate context for the indicators explored throughout the story.

### 2. Climate indicators do not change in isolation

Several environmental indicators show statistical associations with regional temperature anomaly. These relationships help identify patterns in the data, but they are interpreted as associations rather than proof of causation.

### 3. Historical trends point towards continued change

Trend and model comparisons indicate continued changes under the fitted historical relationships. However, projections become increasingly uncertain as they extend further beyond the observed data.

### 4. Statistical significance is not enough

Some indicators showed strong statistical trends but were deliberately excluded from the final climate narrative because their changes may primarily reflect growth in monitoring or reporting infrastructure rather than a direct climate signal.

This distinction is important when turning statistical results into a responsible data story.

---

# Data

The primary dataset used in this project is the **SPC Climate Change Indicators** dataset.

### Source

**Pacific Community (SPC)**

The supplied `Data_CLIMATE_CHANGE.csv` contains the source data used for the analysis.

The original source documentation should be consulted for indicator definitions, data coverage and reporting methodology.

### Regional aggregation

For each indicator, values are aggregated across the reporting Pacific territories for each year to create a regional mean series.

The regional series represents the average reported territorial signal rather than a population-weighted estimate.

Because the number of reporting territories can vary between indicators and years, the resulting regional series should be interpreted with this limitation in mind.

---

# Methodology

The analytical workflow combines descriptive analysis, statistical association, variable selection and trend-based modelling.

## 1. Data preparation

The source dataset is cleaned and standardised before analysis.

The process includes:

- standardising indicator and territory information;
- preparing yearly observations;
- handling available observations across reporting territories;
- constructing regional indicator series.

## 2. Trend analysis

Linear trends are estimated against year for the available indicators.

These trends are used to understand how indicators have changed over time and to provide the historical context for the visual story.

## 3. Correlation analysis

Pearson correlation is used to examine statistical associations between indicators and regional temperature anomaly.

Correlation is treated as an indication of association, **not evidence of causation**.

## 4. Forward selection

Stepwise forward selection is used to identify indicators that provide the strongest contribution to a statistical model of regional temperature anomaly.

The procedure:

1. starts with no predictors;
2. evaluates the remaining candidate indicators;
3. adds the indicator producing the greatest improvement in adjusted R²;
4. continues until the next addition improves adjusted R² by less than 0.005.

The analysis uses the 1995–2022 period where seven candidate indicators overlap, resulting in 28 annual observations.

## 5. Model comparison

For temperature and sea-level indicators, both linear and quadratic polynomial models are fitted.

The models are compared using Akaike Information Criterion (AIC), with the lower AIC indicating the better in-sample fit.

The resulting 2030 and 2050 values are presented as **trend-based modelled projections**, not as precise climate forecasts.

Uncertainty increases as projections extend further beyond the observed period.

---

# Analytical decisions and exclusions

Not every statistically significant indicator was included in the final climate narrative.

Two indicators were deliberately excluded:

- **Meteorological Monitoring Network**
- **Fisheries Management Measures**

Although these indicators showed statistically strong trends, their changes are more plausibly influenced by growth in monitoring, reporting or administrative infrastructure over time.

Including them without this context could incorrectly present changes in reporting capacity as evidence of climate change.

This exclusion was therefore an analytical judgement rather than a statistical failure.

---

# Limitations

Several limitations should be considered when interpreting the results:

- Regional means depend on the territories reporting data in each year.
- Missing observations may affect comparability across indicators and years.
- Territories contribute to the regional mean based on the aggregation approach rather than population size.
- Correlation and regression results indicate statistical association, not causation.
- The forward-selection analysis is based on a relatively small overlapping sample.
- Modelled projections become increasingly uncertain further beyond the observed period.
- The analysis does not attempt to reproduce physical climate models or emissions scenarios.
- Historical statistical relationships should not be interpreted as guaranteed future outcomes.

These limitations are important when translating statistical patterns into a climate narrative.

---

# Reproducible analysis

The repository contains the source dataset, analysis scripts and supporting outputs used to develop the visual story.

The core analysis is implemented in Python using:

- pandas
- NumPy
- SciPy
- Matplotlib

The analysis can be reproduced using the scripts in the `Code` folder.

### Setup

Python 3.9+ is recommended.

Install the required packages:

```bash
pip install pandas numpy scipy matplotlib
