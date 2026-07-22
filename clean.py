import pandas as pd

from utils import ready, load, save_dictionary_to_excel


# ==========================
#       Load Methods
# ==========================

def load_food_expenditure_by_income():
    return load("data/raw/defra_family_food_expenditure_by_income_decile_2024.xlsx")


def load_food_expenditure_by_region():
    return load("data/raw/defra_family_food_expenditure_by_region_2024.xlsx")


def load_regional_gdhi():
    return load("data/raw/ons_regional_gdhi_local_authority_1997-2023.xlsx")


# ==========================
#    Preprocess Methods
# ==========================

def trim_dictionary(dict1, start_index):
    """Trim dictionary by dropping the first N sheets."""
    keys = list(dict1.keys())[start_index:]
    vals = list(dict1.values())[start_index:]
    pp_dict = {}

    for i in range(len(keys)):
        pp_dict[keys[i]] = vals[i]

    return pp_dict


def aggregate_columns():
    """For a given set of columns, replace with a single combined column"""
    pass


def fix_column_typo_expenditure_by_income(dict1):
    """Sheet Decile_6 has a typo in column headings
        Major Food Code...8	Minor Food Code...9
        which should read: 2001-02	2002-03"""
    df = dict1["Decile_6"]

    assert df.iloc[3, 7] == "Major Food Code...8"
    assert df.iloc[3, 8] == "Minor Food Code...9"

    df.iloc[3, 7] = "2001-02"
    df.iloc[3, 8] = "2002-03"

    return dict1


def preprocess_food_expenditure_by_income(dict1):
    """Drop first 2 sheets from excel workbook."""
    return trim_dictionary(dict1, 2)


def process_food_expenditure_by_income(dict1):
    """Drop first 3 rows from each sheet. Copy top row to column names then drop top row. """
    for df in dict1.values():
        df.drop([0,1,2], inplace = True)
        
        df.columns = df.loc[3]
        df.drop(index = 3, inplace = True)
        
    return dict1


def preprocess_food_expenditure_by_region(dict2):
    """Drop first 2 sheets from excel workbook."""
    return trim_dictionary(dict2, 2)


def process_food_expenditure_by_region(dict2):
    """Drop first 3 rows from each sheet. Copy top row to column names then drop top row. """
    for df in dict2.values():
        df.drop([0,1,2], inplace = True)
        
        df.columns = df.loc[3]
        df.drop(index = 3, inplace = True)
        
    return dict2
    

PERIOD_COLUMNS = ['2001-02', '2002-03', '2003-04', '2004-05', '2005-06',
                   2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015,
                   201516, 201617, 201718, 201819, 201920, 202021, 202122, 202223, 202324]


def convert_pence_to_pounds(dict1):
    """Expenditure values are published in pence (Units == 'p'). Convert the
    period columns to pounds so downstream views/measures don't have to
    remember to divide by 100."""
    for df in dict1.values():
        cols = [c for c in PERIOD_COLUMNS if c in df.columns]
        df[cols] = df[cols] / 100

    return dict1


def preprocess_regional_gdhi(dict3):
    """Drop first 3 sheets from excel workbook."""
    return trim_dictionary(dict3, 3)


def process_regional_gdhi(dict3):
    """Copy top row to column names then drop top row."""
    for df in dict3.values():
        df.columns = df.loc[0]
        df.drop(index = 0, inplace = True)
        
    return dict3


# ==========================
#           Main
# ==========================

if __name__ == "__main__":
    ready()

    # Load
    dict1 = load_food_expenditure_by_income()
    dict2 = load_food_expenditure_by_region()
    dict3 = load_regional_gdhi()
    
    print("done loading")

    # Preprocess + process
    p_dict1 = preprocess_food_expenditure_by_income(dict1)
    p_dict1 = fix_column_typo_expenditure_by_income(p_dict1)
    p_dict1 = process_food_expenditure_by_income(p_dict1)
    p_dict1 = convert_pence_to_pounds(p_dict1)

    p_dict2 = preprocess_food_expenditure_by_region(dict2)
    p_dict2 = process_food_expenditure_by_region(p_dict2)
    p_dict2 = convert_pence_to_pounds(p_dict2)

    p_dict3 = preprocess_regional_gdhi(dict3)
    p_dict3 = process_regional_gdhi(p_dict3)
    
    print("processing stages done")
    
    # Save
    save_dictionary_to_excel(p_dict1, "data/processed/defra_family_food_expenditure_by_income_decile_2024.xlsx")
    save_dictionary_to_excel(p_dict2, "data/processed/defra_family_food_expenditure_by_region_2024.xlsx")
    save_dictionary_to_excel(p_dict3, "data/processed/ons_regional_gdhi_local_authority_1997-2023.xlsx")

    print("processed data saved!")

    