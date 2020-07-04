import re

replace_dict = {"custardmonstersalt": 'custard monster',
                'custardmonster':'custard monster',
                'vgodsalt': 'vgod'}

replace_dict_noreg = {'MSRP': '', '(': ' ', ')': ' ',
                      '\&amp;': '', '-': '', '2 x 60ML': '',
                      'E-Liquid': 'Eliquid'}

def clean_name(name, replace_dict):
    '''returns a named with certain substrings removed'''
    for k,v in replace_dict.items():
        name = name.replace(k,v)

    regex_price = re.compile(r"\$(\d+\.\d{1,2})")
    name = re.sub(regex_price, '', name)

    name = ' '.join(name.split())

    name = name.lower()

    return name
