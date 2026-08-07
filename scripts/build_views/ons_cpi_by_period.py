from ..utils import load, dataframe_from_dictionary


# ==========================
#       Load Methods
# ==========================

def load_cpi_index():
    dict1 = load("data/processed/ons_cpi/ons_cpi_index.xlsx")
    return dataframe_from_dictionary(dict1, "Sheet1")


# ==========================
#       Build views
# ==========================

def build_cpi_by_period(df):
    """Already tidy (Period, Value, Series) from the clean step - just
    renamed for clarity on a Power BI chart (Series as legend, Period as
    axis, CPI Index as value)."""
    return df.rename(columns={"Value": "CPI Index"})
