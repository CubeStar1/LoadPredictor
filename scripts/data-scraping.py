import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import csv
from datetime import datetime, timedelta
from ts2ml.core import add_missing_slots

def get_load_data(date):
    load = []
    url = 'http://www.delhisldc.org/Loaddata.aspx?mode='
    print('Scraping ' + date, end=' ')
    resp = requests.get(url + date)
    soup = BeautifulSoup(resp.text, 'lxml')
    table = soup.find('table', {'id':'ContentPlaceHolder3_DGGridAv'})

    try:
        trs = table.findAll('tr')
        if len(trs[1:]):
            with open('load_data_2024_3.csv', 'a') as f:
                writer = csv.writer(f)
                for tr in trs[1:]:
                    time, delhi = tr.findChildren('font')[:2]
                    load.append(delhi.text)
                    writer.writerow([date + ' ' + time.text, delhi.text])
        if len(trs[1:]) != 288:
            print('Some of the load values are missing..')
        else:
            print('Done')
    except:
        print('Some error occured..')
    return load


# Scraping the data
for i in range(31, 0, -1):
    yesterday = datetime.today() - timedelta(i)
    yesterday = yesterday.strftime('%d/%m/%Y')
    get_load_data(yesterday)


# Data Cleaning
data = pd.read_csv('load_data_2024_3.csv', header=None, names=['datetime', 'load'])
data.dropna(inplace=True)
data['datetime'] = pd.to_datetime((data['datetime']),dayfirst=True, format='mixed')
data["day"] = data["datetime"].dt.dayofyear - data["datetime"].dt.dayofyear.min()
def swap_columns(df, col1, col2):
    col_list = list(df.columns)
    x, y = col_list.index(col1), col_list.index(col2)
    col_list[y], col_list[x] = col_list[x], col_list[y]
    df = df[col_list]
    return df

data = swap_columns(data, "load", "day")
df = add_missing_slots(data, datetime_col='datetime', entity_col='day', value_col='load', freq='5min')
output = pd.DataFrame()
for i in range(364):
    df2 = df.loc[df['day'] == i, ["datetime", 'load']][i*288:(i+1)*288]
    output = pd.concat([output, df2])

output = output.replace(0, np.nan)
output = output.fillna(method='ffill')
output.to_csv('load_data_2024_cleaned2.csv', index=False)
