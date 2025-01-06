import os
import sys
import requests # внешний модуль
import xmltodict # внешний модуль

# добавил путь для импорта скрипта который получает url из .env
# и импортировал переменную из скрипта
sys.path.append(os.path.join(os.getcwd(), '../..'))
from env.get_from_env import url_from_env


url = url_from_env
response = requests.get(url)
xml = response.content
xml_dict = xmltodict.parse(xml)
data_securities = xml_dict['document']['data'][0]
data_marketdata = xml_dict['document']['data'][1]
list_securities_names = ["secid", "boardid", "shortname", "prevprice", "lotsize", "facevalue", "boardname", "secname", "prevwaprice", "prevdate", "issuesize", "isin", "latname", "prevlegalcloseprice", "listlevel", "settledate"]
list_marketdata_names = ["open", "low", "high", "last", "value", "value_usd", "waprice", "valtoday", "valtoday_usd"]

def get_stocks_list():
    list_securities = []
    list_marketdata = []
    for rows in data_securities['rows']['row']:
        tmp_securities_list = []
        for key, value in rows.items():
            if key[1:].lower() in list_securities_names:
                if value.isdigit():
                    tmp_securities_list.append(int(value))
                else:
                    try:
                        tmp_securities_list.append(float(value))
                    except:
                        tmp_securities_list.append(value)
        list_securities.append(tmp_securities_list)

    for rows in data_marketdata['rows']['row']:
        tmp_marketdata_list = []
        for key, value in rows.items():
            if key[1:].lower() in list_marketdata_names:
                if not value:
                    tmp_marketdata_list.append(None)
                elif value.isdigit():
                    tmp_marketdata_list.append(int(value))
                else:
                    try:
                        tmp_marketdata_list.append(float(value))
                    except:
                        tmp_marketdata_list.append(value)
        list_marketdata.append(tmp_marketdata_list)
    stocks_list = []
    for value1, value2 in zip(list_securities, list_marketdata):
        stocks_list.append(list(value1 + value2))
    return stocks_list

if __name__ == '__main__':
    print(*get_stocks_list(), sep='\n')


