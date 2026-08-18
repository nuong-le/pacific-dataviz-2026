# Smallest Footprint, Biggest Impact

## Pacific Climate Change — Pacific Dataviz Challenge 2026

The Pacific contributes relatively little to global greenhouse gas emissions, yet Pacific communities are among those facing significant and immediate climate risks.

**Smallest Footprint, Biggest Impact** explores how climate-related indicators are changing across the Pacific, how these indicators relate statistically to regional surface temperature anomalies, and what historical trends suggest about possible future trajectories.

The project combines data preparation, statistical analysis, modelling and interactive visual storytelling to turn a complex set of climate indicators into an accessible evidence-based story.

---

## 🌏 Explore the interactive visualisation

**[▶ View the interactive visualisation](YOUR-GITHUB-PAGES-URL)**

The interactive story brings together long-term temperature and sea-level trends, environmental indicators, statistical relationships, modelled trajectories and potential areas for climate action.

---

## The analytical story

The project follows four stages:

**What is changing? → What moves with temperature? → Which indicators matter most statistically? → What could future trajectories look like?**

The analysis begins by constructing regional yearly series from the available Pacific reporting data. It then examines long-term trends and statistical associations with regional surface temperature anomalies.

A forward-selection model is used to identify which candidate indicators contribute most to explaining variation in the regional temperature series within the available overlapping data.

Finally, linear and quadratic trend models are compared for surface temperature and sea-level anomalies to illustrate possible trajectories to 2030 and 2050.

The statistical results are then translated into an interactive visual narrative.

---

# Key findings

The analysis highlights several patterns that shape the story.

### 1. Surface temperature shows a persistent long-term trend

Regional Surface Temperature anomalies are analysed as the central climate-change reference variable. A linear OLS trend is fitted against year, providing the long-term trend, R² and p-value used in the analysis. :contentReference[oaicite:9]{index=9}

### 2. Climate indicators show different relationships with temperature

Pearson correlations are calculated between each regional indicator series and regional Surface Temperature anomalies using their overlapping years.

These results identify statistical associations in the available data. They are **not interpreted as proof of causation**. :contentReference[oaicite:10]{index=10}

### 3. The strongest statistical contributors are identified through forward selection

A forward-selection procedure starts with an empty model and progressively adds the candidate indicator that produces the greatest improvement in adjusted R² for regional Surface Temperature anomalies.

The procedure stops when the best remaining addition improves adjusted R² by less than 0.005. :contentReference[oaicite:11]{index=11}

### 4. Historical trends can be extended, but projections are uncertain

For Surface Temperature anomalies and Sea Level Anomalies, linear and quadratic polynomial models are fitted and compared using AIC.

The models are then extrapolated to 2030 and 2050 under both functional forms. These are **trend-based statistical projections**, not physical climate-model forecasts or emissions scenarios. :contentReference[oaicite:12]{index=12}

---

# Data

## Primary dataset

The core analysis uses the **SPC Climate Change Indicators** dataset supplied as:

`Data_CLIMATE_CHANGE.csv`

The dataset contains climate and environmental indicators reported for Pacific Island countries and territories.

The analysis pipeline identifies **13 indicators** in the supplied dataset and constructs a regional yearly series for each indicator. :contentReference[oaicite:13]{index=13}

### Regional aggregation

For each indicator, observations are grouped by year and averaged across all territories reporting that indicator in that year.

This produces one regional mean value per year.

The regional mean is therefore an **unweighted mean across available reporting territories**, rather than a population-weighted estimate. :contentReference[oaicite:14]{index=14}

Because reporting coverage can vary across indicators and years, differences in coverage should be considered when interpreting the regional series.

---

# Methodology

## 1. Data preparation

`01_clean_data.py`

The raw SPC CSV is loaded and standardised.

The script:

- selects the required country, indicator, year and observation-value fields;
- removes missing observations;
- standardises country and indicator text;
- identifies the available indicators;
- calculates a yearly regional mean for each indicator.

The output is:

`regional_series.json`

Each indicator is stored as a series of:

```text
[year, value]
