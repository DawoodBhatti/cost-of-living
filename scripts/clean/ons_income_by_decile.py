
from ..utils import load, dataframe_from_dictionary

RAW_DIR = "data/raw/ons_income_by_decile"


def _load_income():
    return load(f"{RAW_DIR}/ons_household_disposable_income_by_decile_fye2024.xlsx")


def _process(df1):
    """Drop first 3 rows from DataFrame. Drop last 2 rows."""
    
    df = df1.copy()
    df.drop(df.index[:3], inplace = True)
    df.drop(df.index[-2:], inplace = True)

    return df


def clean():
    dict1 = _load_income()
    df1 = dataframe_from_dictionary(dict1, "Table 14")
    df1 = _process(df1)
    return df1