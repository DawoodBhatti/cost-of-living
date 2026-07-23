import pandas as pd

RAW_DIR = "data/raw/ons_cpi"

SERIES = {
    "All items": f"{RAW_DIR}/ons_cpi_all_items_d7bt.csv",
    "Food & non-alcoholic beverages": f"{RAW_DIR}/ons_cpi_food_nonalcoholic_d7bu.csv",
}


def _load_annual(path):
    """Load one ONS timeseries CSV and keep only the annual rows.

    ONS's export mixes annual ("1988"), quarterly ("1988 Q1") and monthly
    ("1988 JAN") rows all in one column, after 8 metadata rows (Title, CDID,
    etc). Annual rows are the ones where the period is a bare 4-digit year.
    """
    df = pd.read_csv(path, header = None, names = ["Period", "Value"], skiprows = 8)
    df = df[df["Period"].str.fullmatch(r"\d{4}")].copy()
    df["Period"] = df["Period"].astype(int)
    df["Value"] = df["Value"].astype(float)
    return df


def clean():
    """Return a single tidy DataFrame: Period, Series, Value (CPI index, 2015=100)."""
    frames = []
    for series_name, path in SERIES.items():
        df = _load_annual(path)
        df["Series"] = series_name
        frames.append(df)

    return pd.concat(frames, ignore_index = True)
