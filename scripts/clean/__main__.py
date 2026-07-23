from ..utils import ready, save_dictionary_to_excel, save_dataframe_to_excel

from . import defra_family_food, ons_gdhi, ons_cpi

if __name__ == "__main__":
    ready()

    income = defra_family_food.clean_income()
    region = defra_family_food.clean_region()
    print("defra family food cleaned")

    gdhi = ons_gdhi.clean()
    print("ons gdhi cleaned")

    cpi = ons_cpi.clean()
    print("ons cpi cleaned")

    save_dictionary_to_excel(income, "data/processed/defra_family_food/defra_family_food_expenditure_by_income_decile_2024.xlsx")
    save_dictionary_to_excel(region, "data/processed/defra_family_food/defra_family_food_expenditure_by_region_2024.xlsx")
    save_dictionary_to_excel(gdhi, "data/processed/ons_gdhi/ons_regional_gdhi_local_authority_1997-2023.xlsx")
    save_dataframe_to_excel(cpi, "data/processed/ons_cpi/ons_cpi_index.xlsx")

    print("processed data saved!")
