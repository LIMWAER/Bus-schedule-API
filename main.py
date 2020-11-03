import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import time
import json

url = "https://mybuses.ru/moscow/"
page = requests.get(url)
soup = BeautifulSoup(page.text, 'html.parser')

div = soup.find("div", class_="list-group")


def parse_schedule(a, bus_number):
    url = "https://mybuses.ru" + a["href"]
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    dfs = []
    dic = {}

    def get_rows(table):
        rows = []
        for tr in table.find_all('tr'):
            row = [td.string for td in tr.find_all('td')]
            if len(row) == 0:
                continue
            rows.append(row)
        return rows

    def get_cols(table):
        cols = []
        for th in table.find_all('th'):
            try:
                cols.append(th.a.string)
            except AttributeError:
                cols.append(th.string)
        return cols

    for table in soup.find_all('table'):
        df = pd.DataFrame(data=get_rows(table), columns=get_cols(table))
        df.iloc[:, 0] = df.iloc[:, 0].apply(lambda x: 0 if x == 'выходные' else 1)
        # df.iloc[:,1:] = df.iloc[:,1:].applymap(lambda x: time(int(x.split(':')[0]),int(x.split(':')[1])))
        df.rename(columns={'График / Остановка': 'Будни'}, inplace=True)
        dfs.append(df)

    dic[bus_number] = {"route": dfs[0].to_dict(orient='index'), "return_route": dfs[1].to_dict(orient='index')}
    return dic