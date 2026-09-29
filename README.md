# Forest Fire Danger: A Statistical Prediction Model

Bachelor's thesis project (Process Control, Slovak University of Technology in Bratislava) — a statistical model for predicting forest fire danger from daily weather data, applying the Slovak Hydrometeorological Institute's (SHMÚ) soil-climate drought methodology to a real wildfire season case study in Canada's Northwest Territories.

## Motivation

Forest fires are expected to become more frequent as global temperatures rise, and early detection of dangerous conditions is one of the few practical ways to limit their impact. Several countries run their own fire-danger rating systems — Slovakia's SHMÚ index, Canada's Fire Weather Index (FWI), and Finland's forest fire index — each built on the same idea: estimate how dry the fuel (soil, litter, vegetation) is from routinely available weather data. This project implements the Slovak methodology, applies it to real weather station data from the 2015 Northwest Territories (Canada) wildfire season, and then asks a follow-up question with statistics: of the daily weather variables that go into the index, which ones actually explain most of its variation?

## Methodology

1. **Fire danger index (Ksi)** — computed per the SHMÚ soil-climate drought coefficient method: a linearized Thornthwaite formula estimates reference evapotranspiration (ET0) from mean temperature and day length; the daily climatic water balance (Kz = ET0 − precipitation) accumulates into a balance term (Bi); dividing by the soil's usable water capacity (VWC) gives the drought coefficient Ksi, which maps onto 5 danger classes from "very low" to "extreme" (full derivation in `docs/`).
2. **Case study data** — daily climate observations (temperature, precipitation, humidity, wind) for the YELLOWKNIFE-HENDERSON station, Northwest Territories, covering the 2015 wildfire season (`data/`), sourced from Environment and Climate Change Canada's historical climate data.
3. **Regression modeling** — with Ksi computed for each day, a multiple linear regression was fit in Statgraphics to test which of 6 candidate weather variables (soil water capacity, soil temperature, precipitation, max. temperature, max. wind speed, min. humidity) best predict Ksi. All 57 possible variable-subset models (2–6 variables) were compared by adjusted R² and Mallows' Cp, and backward stepwise elimination (p-to-remove = 0.05) selected the final model.
4. **Reference/comparison datasets** — the classic Cortez & Morais (2007) Montesinho Park (Portugal) forest fires dataset and Canadian National Fire Database records were reviewed alongside the case study for broader context on FWI-based approaches.

## Result

The final model retains 4 of the 6 candidate predictors — usable water capacity (VWC), soil temperature, precipitation, and minimum humidity — and explains the large majority of the variation in the fire danger coefficient:

```
Ksi = 0.0117 − 0.0010·VWC + 0.0078·Soil_T − 0.0433·precipitation + 0.0007·min_humidity
```

| Metric | Value |
|---|---|
| R² | 98.7% |
| Adjusted R² | 97.0% |
| F-statistic (p-value) | 57.9 (p = 0.0036) |
| All 4 coefficients | statistically significant, p < 0.05 |

Precipitation is the strongest single driver (largest standardized effect, most significant p-value), consistent with the index's design around a climatic water balance — confirming that even a simple 4-variable linear model, built on routinely available weather data, captures the index's behavior well over the case-study period.

## Repository contents

```
reproduce_model.py   # Python re-implementation of the final regression, reading the
                      # same processed dataset (statsmodels OLS) — reproduces the
                      # Statgraphics coefficients and R² exactly, for reproducibility
                      # outside of Statgraphics.

data/
  Data.xlsx                              # Processed dataset: raw Canada + Slovakia
                                          # weather records, the Ksi calculation, and
                                          # the "Spracovanie" sheet with the 8 complete
                                          # cases used in the regression.
  en_climate_daily_NT_*.csv              # Raw Environment Canada daily climate data,
                                          # YELLOWKNIFE-HENDERSON station, 2015.
  forestfires.csv                        # Reference dataset: Cortez & Morais (2007)
                                          # Montesinho Park (Portugal) forest fires.
  2015_NWT_fire_progression.kmz          # Fire perimeter progression, 2015 NWT
                                          # wildfire season (geographic context).
  fwi_current.tif                        # Example Canadian FWI raster (reference).

docs/
  Statgraphics_regression_output.pdf     # Full original Statgraphics output: all-subsets
                                          # model comparison, adjusted R²/Cp plots, the
                                          # backward-stepwise selection, and diagnostics.
  Metodika_a_teoreticky_zaklad.docx      # Methodology chapter: fire-danger background,
                                          # the SHMÚ/FWI/Finnish index derivations, and
                                          # the case for linear regression (Slovak).
```

Not included: the ~15 MB of Copernicus CEMS historical FWI reanalysis (NetCDF) explored during background research, and the ~25 MB Canadian National Fire Database point dataset — both public government/Copernicus datasets, not authored, and easily re-downloaded ([Copernicus CDS](https://cds.climate.copernicus.eu/), [Canadian National Fire Database](https://cwfis.cfs.nrcan.gc.ca/ha/nfdb)).

## Running it

```bash
pip install -r requirements.txt
python3 reproduce_model.py
```

## Author

Teodor Noga — [linkedin.com/in/teodor-noga-5a58231a9](https://www.linkedin.com/in/teodor-noga-5a58231a9)
