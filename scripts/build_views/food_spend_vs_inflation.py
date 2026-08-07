import pandas as pd

from ..utils import PERIOD_COLUMNS, parse_defra_period_to_year
from .defra_total_spend_by_decile import load_food_expenditure_by_income
from .ons_cpi_by_period import load_cpi_index


# ==========================
#       Build views
# ==========================

def build_food_spend_by_period(dict1):
    """Average (across all income deciles) total food & drink spend (t1) per
    period. Deciles are equal-population groups, so an unweighted average
    across them is the correct population-wide average, not an approximation."""
    t1_rows = [df.loc[df["Code"] == "t1", PERIOD_COLUMNS] for df in dict1.values()]
    all_deciles = pd.concat(t1_rows, ignore_index = True)

    result = all_deciles.mean().reset_index()
    result.columns = ["Period", "Food Spend (£)"]
    result["Year"] = result["Period"].apply(parse_defra_period_to_year)

    return result


def build_food_spend_vs_inflation(spend_df, cpi_df):
    """Combine average food spend per period with the CPI food sub-index,
    joined on year. Wide format (one column per metric, not long/tidy) since
    the two series are on different scales (£ vs index points) and are meant
    for a dual-axis line chart in Power BI, not a legend-based split.

    Note: `spend_df`'s "t1" DEFRA row is total food+drink spend INCLUDING
    eating out, while the CPI food sub-index (D7BU) covers at-home
    groceries only, not eating out - close but not a perfect category match.
    """
    food_cpi = cpi_df.loc[cpi_df["Series"] == "Food & non-alcoholic beverages", ["Period", "CPI Index"]]
    food_cpi = food_cpi.rename(columns = {"Period": "Year", "CPI Index": "CPI Food Index"})

    merged = spend_df.merge(food_cpi, on = "Year", how = "inner")
    return merged[["Year", "Period", "Food Spend (£)", "CPI Food Index"]]
