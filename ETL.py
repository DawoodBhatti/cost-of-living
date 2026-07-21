import pandas as pd


def ready():
    print("ready to go")


# ==========================
#       Load Methods
# ==========================

def load(filename):
    """Return a dictionary of DataFrames. Each Excel sheet = one DataFrame."""
    return pd.read_excel(filename, sheet_name=None)


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
#    Save Methods
# ==========================

def save_excel(pp_dict, file_dir):
    """save df elements of dictionary to a single excel sheet"""
    
    
    with pd.ExcelWriter(file_dir) as writer:
        for key in pp_dict.keys():
            pp_dict[key].to_excel(writer, sheet_name = key, index = False)
    

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
    p_dict1 = process_food_expenditure_by_income(p_dict1)

    p_dict2 = preprocess_food_expenditure_by_region(dict2)
    p_dict2 = process_food_expenditure_by_region(p_dict2)

    p_dict3 = preprocess_regional_gdhi(dict3)
    p_dict3 = process_regional_gdhi(p_dict3)
    
    print("processing stages done")
    
    # Save
    save_excel(p_dict1, "data/processed/defra_family_food_expenditure_by_income_decile_2024.xlsx")
    save_excel(p_dict2, "data/processed/defra_family_food_expenditure_by_region_2024.xlsx")
    save_excel(p_dict3, "data/processed/ons_regional_gdhi_local_authority_1997-2023.xlsx")

    print("processed data saved!")

    