import pandas as pd

from ..utils import load


# ==========================
#       Load Methods
# ==========================

def load_ons_income_by_decile():
    return load("data/processed/ons_income_by_decile/ons_income_by_decile.xlsx")



# ==========================
#       Build views
# ==========================

def build_average_equivalised_income_per_decile(dict1):
    """Extract single dataframe. set first row to column names. keep last 3 rows only."""

    df = dict1['Sheet1']
    df.columns=df.iloc[0]
    df.drop(df.index[:-2], inplace = True)
    
    return df



    
