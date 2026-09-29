"""
Reproduces the multiple linear regression model from the bachelor thesis
"Statisticky model pre predikciu lesnych poziarov" (Statistical model for
forest fire prediction).

The original model selection and fitting was done in Statgraphics
(see docs/Statgraphics_regression_output.pdf for the original output).
This script reads the same processed dataset (data/Data.xlsx, sheet
"Spracovanie") and refits the same backward-stepwise-selected model with
Python (statsmodels) to make the result independently reproducible.

Target variable:
  Ksi  - soil-climate drought coefficient (Slovak Hydrometeorological
         Institute, SHMU, methodology), computed from daily precipitation
         and a linearized Thornthwaite reference evapotranspiration (ET0),
         normalized by the soil's usable water capacity (VWC).

Predictors in the final model (selected by Statgraphics backward
elimination, p-to-remove = 0.05):
  VWC                    - usable water capacity of the soil [mm]
  Soil_T                 - mean soil/air temperature used in ET0 [deg C]
  zrazky[mm]             - daily precipitation [mm]
  Najnizsia vlhkost[%]   - daily minimum relative humidity [%]

Data: Environment Canada daily climate observations for the
YELLOWKNIFE-HENDERSON station (Northwest Territories, 2015), covering
the period of the 2015 NWT wildfire season.
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm

DATA_FILE = "data/Data.xlsx"
SHEET = "Spracovanie"

TARGET = "Ksi"
PREDICTORS = ["VWC", "Soil_T", "zrážky[mm]", "Najnižšia vlhkosť[%]"]


def load_complete_cases(path=DATA_FILE, sheet=SHEET):
    """Load the processed sheet and keep only the rows with no missing
    values in the target + predictor columns (the 8 complete cases used
    for the regression in the thesis)."""
    raw = pd.read_excel(path, sheet_name=sheet, header=4)
    cols = [TARGET] + PREDICTORS
    df = raw[cols].dropna()
    return df.reset_index(drop=True)


def fit_model(df):
    X = sm.add_constant(df[PREDICTORS])
    y = df[TARGET]
    return sm.OLS(y, X).fit()


def main():
    df = load_complete_cases()
    print(f"Complete cases used: {len(df)}\n")
    print(df.to_string(index=False))
    print()

    model = fit_model(df)
    print(model.summary())

    print("\nFitted equation:")
    c = model.params
    terms = " + ".join(f"{c[p]:.6g}*{p}" for p in PREDICTORS)
    print(f"Ksi = {c['const']:.6g} + {terms}")


if __name__ == "__main__":
    main()
