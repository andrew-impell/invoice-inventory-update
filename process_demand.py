import pandas as pd
import re

# fname='demand_invoice_html.html'
def process_demand_html(fname, invoice_dict):

    dfs = pd.read_html(fname)

    df = dfs[4]

    df = df.iloc[:-5, [0,2]]
    df.index = df.iloc[:, 0]
    df = df.iloc[:, 1:]
    df['Quantity'] = df['Quantity'].astype(int)

    pattern = r'- [0-9]{4,5}:'
    pattern = re.compile(pattern)
    df.index = df.index.str.replace(pattern, "", regex=True)

    df_dict = df.to_dict('index')

    for k, v in df_dict.items():
        q = list(v.items())[0][1]
        invoice_dict[k] = q

    return invoice_dict
