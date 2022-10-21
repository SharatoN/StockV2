import pandas as pd
import numpy as np

def load_data(URL):
    html = pd.read_html(URL,header=0)
    return html[0]


def get_SP500_name():


    df =load_data('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

    data_clear = []

    df = df.Symbol

    for i in range(len(df)):
        data_clear.append(df[i])

    return data_clear