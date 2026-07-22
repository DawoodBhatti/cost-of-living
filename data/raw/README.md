# Raw data

Files as downloaded from source, with one exception noted below.

| File | Source | Original format | Download page |
|---|---|---|---|
| `ons_regional_gdhi_local_authority_1997-2023.xlsx` | ONS | `.xlsx` (unmodified) | [Regional gross disposable household income: local authorities](https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalgrossdisposablehouseholdincomelocalauthorities) |
| `defra_family_food_expenditure_by_region_2024.ods` | DEFRA/GOV.UK | `.ods` (original, unmodified) | [Family food datasets](https://www.gov.uk/government/statistical-data-sets/family-food-datasets) (Countries and Regions expenditure file) |
| `defra_family_food_expenditure_by_income_decile_2024.ods` | DEFRA/GOV.UK | `.ods` (original, unmodified) | [Family food datasets](https://www.gov.uk/government/statistical-data-sets/family-food-datasets) (Equivalised Income Decile expenditure file) |

## Note on the DEFRA `.xlsx` files

The two DEFRA files were originally downloaded as `.ods`. They were manually
converted to `.xlsx` (same content, no data changes) so `clean.py` could load
them with `pd.read_excel()` without an extra `odfpy` dependency. Both the
original `.ods` and the converted `.xlsx` are kept here for provenance —
`clean.py` reads from the `.xlsx` versions.
