import pandas as pd


def ready():
    print("ready to go")


# ==========================
#       Load Methods
# ==========================

def load(filename):
    """Return a dictionary of DataFrames. Each Excel sheet = one DataFrame."""
    return pd.read_excel(filename, sheet_name=None)


def trim_dictionary(dict1, start_index):
    """Trim dictionary by dropping the first N sheets."""
    keys = list(dict1.keys())[start_index:]
    vals = list(dict1.values())[start_index:]
    pp_dict = {}

    for i in range(len(keys)):
        pp_dict[keys[i]] = vals[i]

    return pp_dict


def dataframe_from_dictionary(dict1, target):
    """Extract a single DataFrame from a dictionary"""
    return dict1[target]


PERIOD_COLUMNS = ['2001-02', '2002-03', '2003-04', '2004-05', '2005-06',
                  2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015,
                  201516, 201617, 201718, 201819, 201920, 202021, 202122, 202223, 202324]


def parse_defra_period_to_year(period):
    """Convert a DEFRA period label to its start year as an int.
    Handles dash-separated financial years ("2002-03"), concatenated
    financial years ("201516"), and plain calendar years (2006)."""
    period = str(period)
    if "-" in period:
        return int(period[:4])
    if len(period) == 6:
        return int(period[:4])
    return int(period)


# ==========================
#    Save Methods
# ==========================

def save_dictionary_to_excel(dict_of_dfs, file_dir):
    """Save each DataFrame in a dict to its own sheet in one Excel workbook."""
    with pd.ExcelWriter(file_dir) as writer:
        for sheet_name, df in dict_of_dfs.items():
            df.to_excel(writer, sheet_name = sheet_name, index = False)


def save_dataframe_to_excel(df, file_dir, sheet_name = "Sheet1"):
    """Save a single DataFrame to one sheet in an Excel workbook."""
    save_dictionary_to_excel({sheet_name: df}, file_dir)
