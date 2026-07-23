from ..utils import ready, save_dataframe_to_excel

from . import defra_total_spend_by_decile as view1

if __name__ == "__main__":
    ready()

    # Load
    dict1 = view1.load_food_expenditure_by_income()
    dict2 = view1.load_food_expenditure_by_region()
    dict3 = view1.load_regional_gdhi()
    print("done loading")

    #Build views
    v_df1 = view1.build_total_spend_by_decile(dict1)
    print("views built")

    #Save views
    save_dataframe_to_excel(v_df1, "data/views/defra_total_spend_by_decile.xlsx")

    #print("views saved")
