import numpy as np
import pandas as pd

from .income_distribution_fit import (
    load_ons_income_by_decile,
    get_decile_points,
    get_decile_means,
    fit_lognormal,
    fit_pareto_tail,
)

X_MIN = 100
X_MAX = 300_000
N_POINTS = 3000


# ==========================
#       PDF functions
# ==========================

def lognormal_pdf(x, mu, sigma):
    return (1 / (x * sigma * np.sqrt(2 * np.pi))) * np.exp(-((np.log(x) - mu) ** 2) / (2 * sigma ** 2))


def pareto_pdf(x, x_m, alpha):
    """Only defined for x >= x_m - NaN below that, so Power BI simply
    doesn't draw a Pareto line over the range the lognormal already covers."""
    density = (alpha * x_m ** alpha) / (x ** (alpha + 1))
    return np.where(x >= x_m, density, np.nan)


# ==========================
#       Build views
# ==========================

def build_income_distribution_curve(df):
    """Evaluate the fitted lognormal and Pareto PDFs across a grid of income
    values, for plotting the actual distribution shape (not decile means) in
    Power BI. Reuses the same calibration as income_distribution_fit.py
    rather than re-deriving mu/sigma/x_m/alpha a second time."""
    decile_points = get_decile_points(df)
    decile_means = get_decile_means(df)

    mu, sigma = fit_lognormal(decile_points)
    x_m, alpha = fit_pareto_tail(decile_points, decile_means)

    x = np.linspace(X_MIN, X_MAX, N_POINTS)

    lognormal_df = pd.DataFrame({
        "Income": x,
        "Density": lognormal_pdf(x, mu, sigma),
        "Distribution": "Lognormal",
    })

    pareto_df = pd.DataFrame({
        "Income": x,
        "Density": pareto_pdf(x, x_m, alpha),
        "Distribution": "Pareto (Tail)",
    })

    return pd.concat([lognormal_df, pareto_df], ignore_index = True)


# ==========================
#           Main
# ==========================

if __name__ == "__main__":
    from ..utils import ready, save_dataframe_to_excel

    ready()

    df = load_ons_income_by_decile()
    curve = build_income_distribution_curve(df)

    save_dataframe_to_excel(curve, "data/views/income_distribution_curve.xlsx")
    print("income distribution curve saved")
