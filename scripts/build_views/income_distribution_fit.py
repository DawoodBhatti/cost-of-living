import numpy as np
import pandas as pd

from ..utils import load, dataframe_from_dictionary

# Standard normal 90th-percentile quantile, i.e. Phi^-1(0.9). Hardcoded
# rather than pulling in scipy for one constant.
Z_90 = 1.2815515655446004

N_SIMULATIONS = 1_000_000
RANDOM_SEED = 42


# ==========================
#       Load Methods
# ==========================

def load_ons_income_by_decile():
    dict1 = load("data/processed/ons_income_by_decile/ons_income_by_decile.xlsx")
    return dataframe_from_dictionary(dict1, "Sheet1")


# ==========================
#       Build views
# ==========================

def get_decile_points(df):
    """The 9 decile boundary points (2nd-10th), indexed 2-10."""
    row = df[df.iloc[:, 0] == "Decile points (equivalised £)"].iloc[0]
    points = row.iloc[2:11]
    points.index = range(2, 11)
    return points.astype(float)


def get_decile_means(df):
    """Mean equivalised disposable income per decile group, indexed 1-10."""
    row = df[df.iloc[:, 0] == "Equivalised disposable income"].iloc[0]
    means = row.iloc[1:11]
    means.index = range(1, 11)
    return means.astype(float)


def fit_lognormal(decile_points):
    """Calibrate a lognormal distribution from two known quantiles: the
    median (the 6th decile point, i.e. the 50th percentile boundary) and
    the 90th percentile (the 10th decile point, i.e. the Decile 9/10
    boundary)."""
    median = decile_points[6]
    p90 = decile_points[10]

    mu = np.log(median)
    sigma = (np.log(p90) - mu) / Z_90

    return mu, sigma


def simulate_lognormal_decile_means(mu, sigma):
    """Monte Carlo simulate the lognormal fit, bin into 10 equal-population
    deciles, and return the mean of each simulated decile - this is what
    decile means we'd expect if income were exactly lognormal."""
    rng = np.random.default_rng(RANDOM_SEED)
    samples = rng.lognormal(mean = mu, sigma = sigma, size = N_SIMULATIONS)

    bins = pd.qcut(samples, 10, labels = range(1, 11))
    means = pd.Series(samples).groupby(bins, observed = True).mean()
    means.index = means.index.astype(int)

    return means


def fit_pareto_tail(decile_points, decile_means):
    """Fit a Pareto distribution to Decile 10 specifically, using the
    Decile 9/10 boundary as the Pareto minimum (x_m) and Decile 10's actual
    mean to solve for the shape parameter alpha:
        mean = x_m * alpha / (alpha - 1)  =>  alpha = mean / (mean - x_m)
    """
    x_m = decile_points[10]
    mean = decile_means[10]

    alpha = mean / (mean - x_m)

    return x_m, alpha


def build_income_distribution_fit(df):
    """Compare actual decile-group mean income against a lognormal fit
    (whole distribution) and a Pareto fit (Decile 10 tail only), in one
    tidy table: Decile, Metric, Value. Long format so Power BI can either
    overlay all three as one combo chart or split by Metric into separate
    visuals."""
    decile_points = get_decile_points(df)
    decile_means = get_decile_means(df)

    mu, sigma = fit_lognormal(decile_points)
    lognormal_means = simulate_lognormal_decile_means(mu, sigma)

    x_m, alpha = fit_pareto_tail(decile_points, decile_means)
    # By construction this reproduces decile_means[10] exactly - included
    # as its own row so the "different law at the tail" point is explicit
    # on the chart rather than just implied.
    pareto_tail_mean = x_m * alpha / (alpha - 1)

    rows = []
    for decile in range(1, 11):
        rows.append({"Decile": decile, "Metric": "Actual Mean Income", "Value": decile_means[decile]})

        # Decile 10 is modeled by Pareto, not lognormal - left out here so
        # the chart shows Actual + Pareto for the tail, not all three.
        if decile != 10:
            rows.append({"Decile": decile, "Metric": "Lognormal Fit", "Value": lognormal_means[decile]})

    rows.append({"Decile": 10, "Metric": "Pareto Fit (Tail)", "Value": pareto_tail_mean})

    return pd.DataFrame(rows)
