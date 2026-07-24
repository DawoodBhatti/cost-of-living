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
    """ - Extract single dataframe. 
        - set first row to column names.
        - set index values equal to first column
        - keep last 3 rows only.
        - drop first and last column. 
        - add decile numbers as new row for powerBI plotting.
        - Transpose data for output."""

    df = dict1['Sheet1']
    df.columns=df.iloc[0]
    df.index = df.iloc[:,0]
    df.drop(df.index[:-1], inplace = True)
    df.drop(df.columns[0], axis=1, inplace=True)
    df.drop(df.columns[-1], axis=1, inplace=True)
    df.loc["decile_number"] = [i for i in range(1,11)]
    
    new_col_names = list(df.index.values)
    
    df = df.T
    df.columns = new_col_names
    
    return df



    
