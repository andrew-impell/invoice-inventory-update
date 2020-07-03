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

from process_medusa import process_medusa
from process_midwest import process_midwest_html
from load_update_sheet import load_shopkeep


replace_dict = {"custardmonstersalt": 'custard monster',
                'custardmonster':'custard monster',
                'vgodsalt': 'vgod', 'replacement coils': ''}

replace_dict_noreg = {'MSRP': '', '(': ' ', ')': ' ',
                      '\&amp;': '', '-': '', '2 x 60ML': '',
                      'E-Liquid': 'Eliquid'}


medusa_fname = 'medusa.pdf'


shopkeep_fname = 'norwich_update_test.csv'

copy_df, compare_values = load_shopkeep(shopkeep_fname)

invoice_dict = process_medusa(medusa_fname)
invoice_dict = process_midwest_html('midwest_md.html', invoice_dict)

update_df = pd.DataFrame()

for key, val in invoice_dict.items():

    search_str, add_quant = " ".join(sorted(list(set(key.split())))), int(val)

    fuzzed = process.extract(search_str, compare_values.values,
                             limit=2, scorer=fuzz.partial_ratio)

    if fuzzed[0][0] == 'eliquid sale':
        best = fuzzed[1][0]
    else:
        best = fuzzed[0][0]

    print(key)
    print(f'\t[+] Best Match: {best}', sep='\n')
    print('\n')
