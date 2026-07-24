from ..utils import ready, save_dataframe_to_excel

from . import defra_total_spend_by_decile as view1
from . import ons_income_by_decile as view2

if __name__ == "__main__":
    ready()

    # Load
    dict1 = view1.load_food_expenditure_by_income()
    dict2 = view2.load_ons_income_by_decile()
    print("done loading")

    #Build views
    v_df1 = view1.build_total_spend_by_decile(dict1)
    v_df2 = view2.build_average_equivalised_income_per_decile(dict2)
    print("views built")

    #Save views
    save_dataframe_to_excel(v_df1, "data/views/defra_total_spend_by_decile.xlsx")
    save_dataframe_to_excel(v_df2, "data/views/ons_income_by_decile.xlsx")
    print("views saved to excel")

    #print("views saved")
