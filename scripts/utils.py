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
