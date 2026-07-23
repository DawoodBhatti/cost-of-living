from ..utils import load, trim_dictionary

RAW_DIR = "data/raw/ons_gdhi"


def _load():
    return load(f"{RAW_DIR}/ons_regional_gdhi_local_authority_1997-2023.xlsx")


def _preprocess(dict3):
    """Drop first 3 sheets from excel workbook."""
    return trim_dictionary(dict3, 3)


def _process(dict3):
    """Copy top row to column names then drop top row."""
    for df in dict3.values():
        df.columns = df.loc[0]
        df.drop(index = 0, inplace = True)

    return dict3


def clean():
    dict3 = _load()
    dict3 = _preprocess(dict3)
    dict3 = _process(dict3)
    return dict3
