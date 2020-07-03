import pandas as pd
from bs4 import BeautifulSoup
from utils import clean_name

replace_dict_noreg = {'MSRP': '', '(': ' ', ')': ' ',
                      '\&amp;': '', '-': '', '2 x 60ML': '',
                      'E-Liquid': 'Eliquid'}

product_dict = {}
fname = 'midwest_md.html'

def process_midwest_html(fname, product_dict):

    with open(fname, 'r') as f:
        soup = BeautifulSoup(f)

    product_li = soup.find_all('li', {'class': 'account-listItem'})

    for product in product_li:
        titles = product.find('h5', {"class": "account-product-title"})
        try:
            vars = product.find('dd', {'class': 'definitionList-value'})
            if vars is None:
                name = titles.string
            else:
                name = titles.string + vars.string
            quantity = int(name[0])
            name = name[4:]
            name = clean_name(name, replace_dict_noreg)
            product_dict[name] = quantity
        except AttributeError as e:
            pass

    return product_dict
