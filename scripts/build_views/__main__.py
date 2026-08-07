from ..utils import ready, save_dataframe_to_excel

from . import defra_total_spend_by_decile as view1
from . import ons_income_by_decile as view2
from . import ons_cpi_by_period as view3
from . import food_spend_vs_inflation as view4
from . import income_distribution_fit as view5
from . import income_distribution_curve as view6

if __name__ == "__main__":
    ready()

    # Load
    dict1 = view1.load_food_expenditure_by_income()
    dict2 = view2.load_ons_income_by_decile()
    df3 = view3.load_cpi_index()
    df5 = view5.load_ons_income_by_decile()
    print("done loading")

    #Build views
    v_df1 = view1.build_total_spend_by_decile(dict1)
    v_df2 = view2.build_average_equivalised_income_per_decile(dict2)
    v_df3 = view3.build_cpi_by_period(df3)

    food_spend_by_period = view4.build_food_spend_by_period(dict1)
    v_df4 = view4.build_food_spend_vs_inflation(food_spend_by_period, v_df3)

    v_df5 = view5.build_income_distribution_fit(df5)
    v_df6 = view6.build_income_distribution_curve(df5)
    print("views built")

    #Save views
    save_dataframe_to_excel(v_df1, "data/views/defra_total_£_spend_by_decile.xlsx")
    save_dataframe_to_excel(v_df2, "data/views/ons_equivalised_income_by_decile.xlsx")
    save_dataframe_to_excel(v_df3, "data/views/ons_cpi_by_period.xlsx")
    save_dataframe_to_excel(v_df4, "data/views/food_spend_vs_inflation.xlsx")
    save_dataframe_to_excel(v_df5, "data/views/income_distribution_fit.xlsx")
    save_dataframe_to_excel(v_df6, "data/views/income_distribution_curve.xlsx")
    print("views saved to excel")

    #print("views saved")
