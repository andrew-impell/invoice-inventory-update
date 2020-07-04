import numpy as np
import pandas as pd

def load_shopkeep(fname):
    '''Returns a copy of the master dataframe and a series of cleaned names'''

    master_df = pd.read_csv(
        fname, encoding='cp1252', header=0)

    # Create a copy of the full dataframe
    copy_df = master_df.copy()
    copy_df.index = copy_df['Item UUID']

    # replace nan option columns with empty string
    master_df['Option1 Value (Do Not Edit)'].replace(to_replace={np.nan: ''}, inplace=True)
    master_df['Option2 Value (Do Not Edit)'].replace(to_replace={np.nan: ''}, inplace=True)

    # create a new column with the option values appended
    master_df['full'] = master_df['Name'] + " " + master_df['Option1 Value (Do Not Edit)']
    master_df['full'] = master_df['full'] + " " + master_df['Option2 Value (Do Not Edit)']

    # cleane the new column
    f = lambda x: " ".join(sorted(list(set(x.split()))))
    master_df['sorted'] = master_df['full'].apply(f)
    master_df['sorted'] = master_df['sorted'].str.lower()

    # set the index
    master_df.index = master_df['Item UUID']

    # create a series to fuzz invoice values with
    compare_values = master_df['sorted']

    return copy_df, compare_values
