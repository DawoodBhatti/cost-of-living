# Cost of Living: Regional Income vs. Food Spend (UK)

A Power BI project exploring how UK household food spending compares to regional
income, using official government data.

## Data sources

| Source | Dataset | Geography | Latest edition |
|---|---|---|---|
| ONS | [Regional gross disposable household income: local authorities](https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalgrossdisposablehouseholdincomelocalauthorities) | Local authority (361 areas) | 1997–2023, published 10 Sep 2025 |
| DEFRA / GOV.UK | [Family Food: expenditure by region](https://www.gov.uk/government/statistical-data-sets/family-food-datasets) | 12 UK regions | FYE 2024, published 17 Mar 2026 |
| DEFRA / GOV.UK | [Family Food: expenditure by income decile](https://www.gov.uk/government/statistical-data-sets/family-food-datasets) | UK-wide, by income decile | FYE 2024, published 17 Mar 2026 |

Raw downloads live in `data/raw/` (gitignored — re-download from the links above
rather than committing them).

### Why the income data stops at 2023

Regional GDHI isn't a gap in this project's data collection — it's the most
current edition ONS has published. Regional GDHI is compiled from detailed
regional economic accounts, so it's released on a ~2-year lag: the 2023-data
edition came out 10 September 2025, and the accompanying reference tables were
published 14 April 2025. The next edition (2024 data) isn't due until
**September 2026**. Any analysis here reflects that lag rather than an
oversight in sourcing.

## Pipeline

1. **Cleansing (Python/pandas)** — raw ONS/DEFRA spreadsheets are cleaned and
   reshaped into tidy CSVs in `data/processed/`.
2. **Visualization (Power BI)** — the processed CSVs are loaded into Power BI
   for the dashboard.

## Status

Early stage — data sourced, cleansing pipeline not yet built.
