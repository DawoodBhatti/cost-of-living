import pandas as pd

from utils import ready, load, save_dataframe_to_excel


# ==========================
#       Load Methods
# ==========================

def load_food_expenditure_by_income():
    return load("data/processed/defra_family_food_expenditure_by_income_decile_2024.xlsx")


def load_food_expenditure_by_region():
    return load("data/processed/defra_family_food_expenditure_by_region_2024.xlsx")


def load_regional_gdhi():
    return load("data/processed/ons_regional_gdhi_local_authority_1997-2023.xlsx")



# ==========================
#       Build views
# ==========================

def build_total_spend_by_decile(dict1):
    """collect all rows with code t1, corresponding to total spend"""
    
    df_total = pd.DataFrame()
    
    period_cols = ['2001-02', '2002-03', '2003-04', '2004-05', '2005-06',
                   2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015,
                   201516, 201617, 201718, 201819, 201920, 202021, 202122, 202223, 202324]
 
    #find code t1 which corresponds to total spend and extract the periods
    for name, df in dict1.items():
        
        print("working on : ", name)
        
        df_temp = df.loc[df["Code"] == "t1"][period_cols]
        df_temp["Decile"]=name
       
        df_total = pd.concat([df_total, df_temp])
    
    return df_total


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

    #Build views
    v_df1 = build_total_spend_by_decile(dict1)
    print("views built")
    
    #Save views
    save_dataframe_to_excel(v_df1, "data/views/defra_total_spend_by_decile.xlsx")

    #print("views saved")



