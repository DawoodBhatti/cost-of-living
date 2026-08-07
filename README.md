# Cost of Living: UK Food Spend Analysis

A Power BI project exploring UK household food spending — by income decile and
region — compared against income and inflation, using official government data.

## Data sources

| Source | Dataset | Geography | Latest edition | Status |
|---|---|---|---|---|
| DEFRA / GOV.UK | [Family Food: expenditure by income decile](https://www.gov.uk/government/statistical-data-sets/family-food-datasets) | UK-wide, by income decile | FYE 2024, published 17 Mar 2026 | In use |
| DEFRA / GOV.UK | [Family Food: expenditure by region](https://www.gov.uk/government/statistical-data-sets/family-food-datasets) | 12 UK regions | FYE 2024, published 17 Mar 2026 | In use |
| ONS | [Regional gross disposable household income: local authorities](https://www.ons.gov.uk/economy/regionalaccounts/grossdisposablehouseholdincome/datasets/regionalgrossdisposablehouseholdincomelocalauthorities) | Local authority (361 areas) | 1997–2023, published 10 Sep 2025 | Downloaded, parked for now (not used in any view) |
| ONS | [CPI Index, All items (D7BT)](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bt/mm23) | UK-wide | Monthly, to Jun 2026 | In use |
| ONS | [CPI Index, Food & non-alcoholic beverages (D7BU)](https://www.ons.gov.uk/economy/inflationandpriceindices/timeseries/d7bu/mm23) | UK-wide | Monthly, to Jun 2026 | In use |
| ONS | [Effects of taxes and benefits on household income (decile points/means)](https://www.ons.gov.uk/peoplepopulationandcommunity/personalandhouseholdfinances/incomeandwealth/datasets/householddisposableincomeandinequality) | UK-wide, by income decile | FYE 2023/24, published 2 May 2025 | In use |

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
figures attached. This ONS dataset gives the actual average equivalised
disposable income for each decile group (FYE 2023/24 prices), so a chart axis
can show "Decile 1 (~£10.7k)" instead of just "Decile 1". It's from a
different ONS survey than DEFRA's own (see
[`data/raw/README.md`](data/raw/README.md) for the caveat on that), used here
as a close approximation rather than an exact match.

### Food spend vs. inflation: two caveats worth knowing

`food_spend_vs_inflation.xlsx` compares DEFRA's total food+drink spend (the
`t1` row, averaged across all deciles) against the CPI food sub-index (D7BU).
Two things worth being upfront about:

- **Category scope differs slightly** — DEFRA's `t1` includes eating out
  (restaurants/takeaways) as well as groceries, while the CPI food sub-index
  covers at-home groceries only. Close, not a perfect match.
- **2015 appears twice** — DEFRA's period labels include both a `2015`
  (calendar year) and a `201516` (financial year) column, which both parse to
  the same start year. The view keeps both rows (distinguishable by the
  `Period` column) rather than silently dropping one — decide in Power BI
  whether to filter one out or plot by `Period` instead of `Year`.

### Why the income distribution needs two different models

Plotting decile 9 → 10 next to decile 1 → 9 shows a striking gap: the jump
from Decile 9 to Decile 10 alone (~£45k) is nearly as large as the entire
cumulative climb from Decile 1 to Decile 9 (~£52k). This isn't a fluke of
this dataset — income (and even more so wealth) distributions are widely
modeled as **lognormal in the body and Pareto (power-law) in the top tail**,
a well-established pattern in income economics. `income_distribution_fit.xlsx`
tests this directly: a lognormal fit calibrated from the median and 90th
percentile decile points, Monte Carlo simulated into decile means, compared
against the actual decile means. Result — lognormal tracks Deciles 4-9
almost exactly (under 0.3% off), but underestimates Decile 10 by ~14% (a
Pareto fit calibrated to the Decile 9/10 boundary matches it exactly instead)
and overestimates Decile 1 by ~40% (the bottom of real income distributions
also deviates from lognormal, typically due to benefit-floor effects). Long
format (Decile, Metric, Value) so it can be plotted either as one overlay
chart (actual vs. both fits) or as separate visuals tied together by this
explanation.

`income_distribution_curve.xlsx` is the companion visual — the actual smooth
PDF curve shape (not decile means), evaluated across a grid of income values
using the same calibrated parameters as `income_distribution_fit.py` (no
parameters re-derived, imported directly to avoid drift between the two).
Lognormal is evaluated across the full range; Pareto is only evaluated for
income ≥ the Decile 9/10 boundary (`NaN` below that), so a line chart only
draws the Pareto curve where it's actually meant to apply. This one can also
be run standalone: `python -m scripts.build_views.income_distribution_curve`.

## Folder structure

```
data/
  raw/<dataset>/          # untouched downloads, one subfolder per source
  processed/<dataset>/    # cleaned, still source-shaped (produced by scripts/clean)
  views/                  # reshaped/combined tables ready for Power BI (produced by scripts/build_views)

scripts/                  # all pipeline code lives here
  utils.py                 # shared load/save/trim/period-parsing helpers used across both packages below
  clean/                    # raw -> processed, one module per dataset
    __main__.py              # orchestrator - run with `python -m scripts.clean`
    defra_family_food.py
    ons_gdhi.py
    ons_cpi.py
    ons_income_by_decile.py
  build_views/               # processed -> views, one module per view
    __main__.py               # orchestrator - run with `python -m scripts.build_views`
    defra_total_spend_by_decile.py
    ons_income_by_decile.py
    ons_cpi_by_period.py
    food_spend_vs_inflation.py
    income_distribution_fit.py
    income_distribution_curve.py
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

Six views are built and ready to plot in Power BI:
- `defra_total_£_spend_by_decile.xlsx` — food+drink spend by decile, by period
- `ons_equivalised_income_by_decile.xlsx` — average income by decile group
- `ons_cpi_by_period.xlsx` — headline and food CPI, by year
- `food_spend_vs_inflation.xlsx` — food spend vs. the CPI food sub-index, by year (see caveats above) — deprioritized for now
- `income_distribution_fit.xlsx` — actual decile means vs. lognormal/Pareto fits (see explanation above)
- `income_distribution_curve.xlsx` — the fitted lognormal/Pareto PDF curves themselves, for the smooth distribution-shape visual

GDHI data is cleaned but currently parked (not used in any view).
