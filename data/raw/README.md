# Raw data

Files as downloaded from source, with one exception noted below. Organized into
one subfolder per dataset.

| File | Source | Original format | Download page |
|---|---|---|---|
| `ons_gdhi/ons_regional_gdhi_local_authority_1997-2023.xlsx` | ONS | `.xlsx` (unmodified) | [Regional gross disposable household income: local authorities](https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalgrossdisposablehouseholdincomelocalauthorities) |
| `defra_family_food/defra_family_food_expenditure_by_region_2024.ods` | DEFRA/GOV.UK | `.ods` (original, unmodified) | [Family food datasets](https://www.gov.uk/government/statistical-data-sets/family-food-datasets) (Countries and Regions expenditure file) |
| `defra_family_food/defra_family_food_expenditure_by_income_decile_2024.ods` | DEFRA/GOV.UK | `.ods` (original, unmodified) | [Family food datasets](https://www.gov.uk/government/statistical-data-sets/family-food-datasets) (Equivalised Income Decile expenditure file) |
| `ons_cpi/ons_cpi_all_items_d7bt.csv` | ONS | `.csv` (unmodified) | [CPI INDEX 00: ALL ITEMS 2015=100 (D7BT)](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23) |
| `ons_cpi/ons_cpi_food_nonalcoholic_d7bu.csv` | ONS | `.csv` (unmodified) | [CPI INDEX 01: FOOD AND NON-ALCOHOLIC BEVERAGES 2015=100 (D7BU)](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bu/mm23) |
| `ons_income_by_decile/ons_household_disposable_income_by_decile_fye2024.xlsx` | ONS | `.xlsx` (unmodified) | [The effects of taxes and benefits on household income, disposable income estimate](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/datasets/householddisposableincomeandinequality) |

## Note on the DEFRA `.xlsx` files

The two DEFRA files were originally downloaded as `.ods`. They were manually
converted to `.xlsx` (same content, no data changes) so `clean/defra_family_food.py`
could load them with `pd.read_excel()` without an extra `odfpy` dependency.
Both the original `.ods` and the converted `.xlsx` are kept here for
provenance — `clean/defra_family_food.py` reads from the `.xlsx` versions.

## Note on CPI data

CPI series (D7BT, D7BU) are monthly index values (2015=100), not currency
amounts — see the project README for how they're compared against the DEFRA
expenditure figures. `clean/ons_cpi.py` keeps only the annual rows (ONS's
export mixes annual/quarterly/monthly periods in one column); no view uses
this data yet.

## Note on income-by-decile data

This is a large multi-table ONS workbook (32 sheets covering many different
breakdowns) — the two sheets actually relevant to labeling DEFRA's
`Decile_1`...`Decile_10` sheets with real £ figures are:

- **Table 3** — "Timeseries of decile points of median equivalised disposable
  household income, 1977-2023/24, UK" — gives the £ income value at each
  decile boundary, one row per year. The most recent row (2023/24) gives the
  boundaries between deciles (e.g. the 2nd decile point, £16,874, is the
  boundary between Decile 1 and Decile 2). There's no explicit boundary below
  Decile 1 or above Decile 10 (open-ended at both ends).
- **Table 14** — "Average household incomes, taxes and benefits of ALL
  individuals by decile group, 2023/24" — gives mean income per decile group
  directly, rather than the boundary points.

**Caveat worth keeping in mind:** this comes from ONS's "Effects of Taxes and
Benefits" survey, not the Living Costs and Food Survey that DEFRA's Family
Food income deciles are actually built from. Both use the same equivalisation
methodology (OECD-modified scale) and should be broadly comparable, but
they're two different surveys of the population, so treat this as a close
approximate guide to what each DEFRA decile represents rather than a
guaranteed exact match. No cleaning script exists for this yet — Ali is
writing it himself.
