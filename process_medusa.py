import tabula
import pandas as pd


replace_dict = {"custardmonstersalt": 'custard monster',
                'custardmonster':'custard monster',
                'vgodsalt': 'vgod'}

def process_one_page_medusa(page, replace_dict):

    d2 = {
        r'(\b){}(\b)'.format(k):r'\1{}\2'.format(v) for k,v in replace_dict.items()}

    if page.empty:
        return None


    if page.shape[0] > 20:

        over = page
        over.dropna(how='any', axis=0, inplace=True)
        over['SKU'] = over['SKU'].str.replace('-', ' ')
        first_words = over['SKU'].apply(lambda x: x.split())
        first_words = first_words.str.get(0)
        over['full'] = first_words + " " + over['Name']
        over['full'] = over['full'].str.replace('-', "")
        over['full'] = over['full'].str.replace('  ', ' ')
        over['full'] = over['full'].str.replace('(' , "")
        over['full'] = over['full'].str.replace(')' , "")
        over['full'] = over['full'].str.replace('E-Liquid' , "Eliquid")
        over['full'] = over['full'].str.lower()


        over['full'] = over['full'].replace(d2, regex=True)

        over = over.iloc[::2, :]
        over = over.iloc[:-2, :]

        over.index = over['full']

        return over['Quantity']

    else:
        page = page.iloc[2:-2, :3]
        cols = ['SKU', 'Name', 'Quantity']
        page.columns = cols
        # page.index = page['SKU']
        # page = page.iloc[: ,1: ]

        # clean SKU
        page['SKU'] = page['SKU'].str.replace(r'\r', "")
        page['SKU'] = page['SKU'].str.replace('-', " ")

        page = page[~page['SKU'].str.contains(r'Page [1-9] of')]
        page['SKU'] = page['SKU'].str.lower()

        # clean name column
        page['Name'] = page['Name'].str.replace('-' , "")
        page['Name'] = page['Name'].str.replace('(' , "")
        page['Name'] = page['Name'].str.replace(')' , "")
        page['Name'] = page['Name'].str.replace('E-Liquid' , "Eliquid")
        page['Name'] = page['Name'].str.lower()

        # clean Quantity
        page['Quantity'] = page['Quantity'].astype('int')

        page['full'] = page['SKU'] + ' ' + page['Name']
        page['full'] = page['full'].replace(d2, regex=True)
        # clean full
        page['full'] = page['full'].str.split()

        f = lambda x: " ".join(sorted(set(x), key=x.index))
        page['full'] = page['full'].apply(f)

        page.index = page['full']

        return page['Quantity']

def process_medusa(fname):

    medusa = tabula.read_pdf(fname, pages='all')


    df_list = []

    for page in medusa:
        df_list.append(process_one_page_medusa(page, replace_dict))

    df_list.remove(None)

    all_pages = pd.concat(df_list, axis=0)

    invoice_dict = all_pages.to_dict()

    return invoice_dict
