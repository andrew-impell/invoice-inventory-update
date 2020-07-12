import glob
import numpy as np
import tabula
import pandas as pd
import random
import string
import re
from bs4 import BeautifulSoup
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import matplotlib.pyplot as plt
from matplotlib import style

from process_medusa import process_medusa
from process_midwest import process_midwest_html
from load_update_sheet import load_shopkeep
from process_demand import process_demand_html

style.use('ggplot')


replace_dict = {"custardmonstersalt": 'custard monster',
                'custardmonster':'custard monster',
                'vgodsalt': 'vgod', 'replacement coils': ''}

replace_dict_noreg = {'MSRP': '', '(': ' ', ')': ' ',
                      '\&amp;': '', '-': '', '2 x 60ML': '',
                      'E-Liquid': 'Eliquid'}




medusa_fname = 'medusa.pdf'
shopkeep_fname = 'norwich_update_test.csv'
midwest_fname = 'midwest_md.html'
demand_fname='demand_invoice_html.html'


copy_df, compare_values = load_shopkeep(shopkeep_fname)

invoice_dict = process_medusa(medusa_fname)
invoice_dict = process_midwest_html(midwest_fname, invoice_dict)
invoice_dict = process_demand_html(demand_fname, invoice_dict)

update_df = pd.DataFrame()

scores = []

for key, val in invoice_dict.items():

    search_str, add_quant = " ".join(sorted(list(set(key.split())))), int(val)

    fuzzed = process.extract(search_str, compare_values.values,
                             limit=2, scorer=fuzz.partial_ratio)


    if fuzzed[0][0] == 'eliquid sale':
        best = fuzzed[1][0]
        best_score = fuzzed[1][1]
    else:
        best = fuzzed[0][0]
        best_score = fuzzed[0][1]

    scores.append(best_score)

    match_uuid = compare_values[compare_values == best].index.values[0]
    copy_df.loc[match_uuid, 'Quantity'] = copy_df.loc[match_uuid]['Quantity'].astype(int) + int(val)
    concat_list = [update_df, copy_df[copy_df.index == match_uuid]]
    update_df = pd.concat(concat_list, axis=0)

    print(key)
    print(f'\t[+] Best Match: {best}', sep='\n')
    print('\n')

print(update_df)

plt.hist(scores, bins=13, density=True)
plt.show()
