import re

def clean_name(name, replace_dict):
    for k,v in replace_dict.items():
        name = name.replace(k,v)

    regex_price = re.compile(r"\$(\d+\.\d{1,2})")
    name = re.sub(regex_price, '', name)

    name = ' '.join(name.split())

    name = name.lower()

    return name
