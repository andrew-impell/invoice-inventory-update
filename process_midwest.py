import pandas as pd
from bs4 import BeautifulSoup
from utils import clean_name, replace_dict_noreg

product_dict = {}
fname = 'midwest_md.html'

def process_midwest_html(fname, product_dict):
    '''Process the midwest html file'''
    with open(fname, 'r') as f:
        soup = BeautifulSoup(f)

    product_li = soup.find_all('li', {'class': 'account-listItem'})

    for product in product_li:
        titles = product.find('h5', {"class": "account-product-title"})
        try:
            # add any variables if there are any
            vars = product.find_all('dd', {'class': 'definitionList-value'})
            vars = " ".join([v.string for v in vars])
            if vars is None:
                name = titles.string
            else:
                name = titles.string + vars
            # change quantity to int
            quantity = int(name[0])
            name = name[4:]
            # clean name
            name = clean_name(name, replace_dict_noreg)
            # add to dict
            product_dict[name] = quantity
        except AttributeError as e:
            pass

    return product_dict
