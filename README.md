# Cost of Living: UK Food Spend Analysis

A Power BI project exploring UK household food spending — by income decile and
region — compared against income and inflation, using official government data.

## Data sources

| Source | Dataset | Geography | Latest edition | Status |
|---|---|---|---|---|
| DEFRA / GOV.UK | [Family Food: expenditure by income decile](https://www.gov.uk/government/statistical-data-sets/family-food-datasets) | UK-wide, by income decile | FYE 2024, published 17 Mar 2026 | In use |
| DEFRA / GOV.UK | [Family Food: expenditure by region](https://www.gov.uk/government/statistical-data-sets/family-food-datasets) | 12 UK regions | FYE 2024, published 17 Mar 2026 | In use |
| ONS | [Regional gross disposable household income: local authorities](https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalgrossdisposablehouseholdincomelocalauthorities) | Local authority (361 areas) | 1997–2023, published 10 Sep 2025 | Downloaded, parked for now (not used in any view) |
| ONS | [CPI Index, All items (D7BT)](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23) | UK-wide | Monthly, to Jun 2026 | Cleaned (annual rows only), not yet used in a view |
| ONS | [CPI Index, Food & non-alcoholic beverages (D7BU)](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bu/mm23) | UK-wide | Monthly, to Jun 2026 | Cleaned (annual rows only), not yet used in a view |
| ONS | [Effects of taxes and benefits on household income (decile points)](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/datasets/householddisposableincomeandinequality) | UK-wide, by income decile | FYE 2023/24, published 2 May 2025 | Downloaded, not yet processed |

Raw downloads live in `data/raw/<dataset>/` — one subfolder per source
(`ons_gdhi/`, `defra_family_food/`, `ons_cpi/`, `ons_income_by_decile/`), see
[`data/raw/README.md`](data/raw/README.md) for exact files and links.
Data is tracked in git (not gitignored), so the repo is self-contained.

### Why the GDHI income data stops at 2023

Regional GDHI isn't a gap in this project's data collection — it's the most
current edition ONS has published. Regional GDHI is compiled from detailed
regional economic accounts, so it's released on a ~2-year lag: the 2023-data
edition came out 10 September 2025, and the accompanying reference tables were
published 14 April 2025. The next edition (2024 data) isn't due until
**September 2026**. Any analysis here reflects that lag rather than an
oversight in sourcing.

### CPI is an index, not a currency figure

The CPI series are indexed to 2015=100 and represent relative price-level
change over time, not £ amounts. Comparing them against DEFRA's £ expenditure
figures means rebasing both to a common start period (% change since year X),
not comparing raw numbers directly. It's also worth being upfront that this
ends up as a **spend-vs-price** comparison rather than a like-for-like price
comparison: DEFRA's expenditure figures reflect both price changes *and*
household behavior changes (buying more/less, trading down to cheaper items),
not price movement alone.

### What the income-by-decile £ ranges are for

DEFRA's `Decile_1`...`Decile_10` sheets are just labeled by number — no £
figures attached. This ONS dataset gives the actual income boundary at each
decile (e.g. Decile 1 = below £16,874/year, Decile 10 = above £71,077/year,
FYE 2023/24 prices), so a chart axis can show "Decile 1 (<£16.9k)" instead of
just "Decile 1". It's from a different ONS survey than DEFRA's own (see
[`data/raw/README.md`](data/raw/README.md) for the caveat on that), used here
as a close approximation rather than an exact match.

## Folder structure

```
data/
  raw/<dataset>/          # untouched downloads, one subfolder per source
  processed/<dataset>/    # cleaned, still source-shaped (produced by scripts/clean)
  views/                  # reshaped/combined tables ready for Power BI (produced by scripts/build_views)

scripts/                  # all pipeline code lives here
  utils.py                 # shared load/save/trim helpers used across both packages below
  clean/                    # raw -> processed, one module per dataset
    __main__.py              # orchestrator - run with `python -m scripts.clean`
    defra_family_food.py
    ons_gdhi.py
    ons_cpi.py
  build_views/               # processed -> views, one module per view
    __main__.py               # orchestrator - run with `python -m scripts.build_views`
    defra_total_spend_by_decile.py
```

## Pipeline

Run both commands from the repo root (not from inside `scripts/`) — the
relative imports and the `data/...` paths both depend on that.

1. **Cleansing (`scripts/clean`, Python/pandas, run with `python -m scripts.clean`)** —
   raw ONS/DEFRA spreadsheets are cleaned and reshaped into tidy tables in
   `data/processed/<dataset>/`. One module per dataset, each exposing a small
   `clean()`-style entry point; `__main__.py` orchestrates all of them and
   saves the output.
2. **View-building (`scripts/build_views`, Python/pandas, run with
   `python -m scripts.build_views`)** — processed tables are combined/reshaped
   into analysis-ready tables in `data/views/`, one module per chart or
   analytical question.
3. **Visualization (Power BI)** — the view tables are loaded into Power BI for
   the dashboard; Power BI is used for visualization only, not data cleaning.

## Status

DEFRA food-spend data is cleaned and has one view built (total spend by
decile). CPI data is downloaded and cleaned (annual values only) but not yet
used in a view. GDHI data is cleaned but currently parked (not used in any
view). Income-by-decile data is downloaded, not yet cleaned — Ali is writing
that cleaning/view-building code himself, to extract decile £ ranges into a
view for labeling the decile chart.
