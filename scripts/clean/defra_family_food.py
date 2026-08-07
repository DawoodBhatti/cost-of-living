from ..utils import load, trim_dictionary, PERIOD_COLUMNS

RAW_DIR = "data/raw/defra_family_food"


def _load_income():
    return load(f"{RAW_DIR}/defra_family_food_expenditure_by_income_decile_2024.xlsx")


def _load_region():
    return load(f"{RAW_DIR}/defra_family_food_expenditure_by_region_2024.xlsx")


def _fix_column_typo(dict1):
    """Sheet Decile_6 has a typo in column headings
        Major Food Code...8	Minor Food Code...9
        which should read: 2001-02	2002-03"""
    df = dict1["Decile_6"]

    assert df.iloc[3, 7] == "Major Food Code...8"
    assert df.iloc[3, 8] == "Minor Food Code...9"

    df.iloc[3, 7] = "2001-02"
    df.iloc[3, 8] = "2002-03"

    return dict1


def _process(dict1):
    """Drop first 3 rows from each sheet. Copy top row to column names then drop top row."""
    for df in dict1.values():
        df.drop([0, 1, 2], inplace = True)

        df.columns = df.loc[3]
        df.drop(index = 3, inplace = True)

    return dict1


def _convert_pence_to_pounds(dict1):
    """Expenditure values are published in pence (Units == 'p'). Convert the
    period columns to pounds so downstream views/measures don't have to
    remember to divide by 100."""
    for df in dict1.values():
        cols = [c for c in PERIOD_COLUMNS if c in df.columns]
        df[cols] = df[cols] / 100

    return dict1


def clean_income():
    dict1 = _load_income()
    dict1 = trim_dictionary(dict1, 2)
    dict1 = _fix_column_typo(dict1)
    dict1 = _process(dict1)
    dict1 = _convert_pence_to_pounds(dict1)
    return dict1


def clean_region():
    dict2 = _load_region()
    dict2 = trim_dictionary(dict2, 2)
    dict2 = _process(dict2)
    dict2 = _convert_pence_to_pounds(dict2)
    return dict2
