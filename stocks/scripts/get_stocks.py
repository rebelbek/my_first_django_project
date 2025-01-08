import os
import sys
import requests # внешний модуль
import xmltodict # внешний модуль

# добавил путь для импорта скрипта который получает url из .env
# и импортировал переменную из скрипта
sys.path.append(os.path.join(os.getcwd(), '../..'))
from env.get_from_env import url_stocks, url_stock


def get_data(url: dict):
    url = url
    response = requests.get(url)
    xml = response.content
    xml_dict = xmltodict.parse(xml)
    data_securities = xml_dict['document']['data'][0]
    data_marketdata = xml_dict['document']['data'][1]
    data = [data_securities, data_marketdata]
    return data


def get_data_for_all(data: list, stocks_fields: dict) -> dict:
    result = []
    for rows in data['rows']['row']:
        tmp_dict= {}
        for key, value in rows.items():
            if key[1:].lower() in stocks_fields:
                if not value:
                    tmp_dict[key[1:].lower()] = None
                elif value.isdigit():
                    tmp_dict[key[1:].lower()] = int(value)
                else:
                    try:
                        tmp_dict[key[1:].lower()] = float(value)
                    except:
                        tmp_dict[key[1:].lower()] = value
        result.append(tmp_dict)
    return result


def get_data_for_one(data: list, stocks_fields: dict) -> dict:
     tmp_dict = {}
     for key, value in data['rows']['row'].items():
         if key[1:].lower() in stocks_fields:
             if not value:
                 tmp_dict[key[1:].lower()] = None
             elif value.isdigit():
                 tmp_dict[key[1:].lower()] = int(value)
             else:
                 try:
                     tmp_dict[key[1:].lower()] = float(value)
                 except:
                     tmp_dict[key[1:].lower()] = value
     return tmp_dict


def get_stocks_dict(stocks_fields: dict) -> dict:
    data = get_data(url_stocks)
    if 'secname' in stocks_fields:
        result = get_data_for_all(data[0], stocks_fields)
    else:
        result = get_data_for_all(data[1], stocks_fields)
    return result


def get_stock_dict(stocks_fields: dict) -> dict:
    url = url_stock.replace('{BOARDID}', stocks_fields['boardid']).replace('{TICKER}', stocks_fields['secid'])
    data = get_data(url)
    if 'secname' in stocks_fields:
        result = get_data_for_one(data[0], stocks_fields)
    else:
        result = get_data_for_one(data[1], stocks_fields)
    return result

# для проверок
if __name__ == '__main__':
    lst = get_data(url_stock.replace('{BOARDID}', 'TQBR').replace('{TICKER}', 'ABIO'))
    print(lst[0]['rows']['row'])
    print(get_data_for_one(lst[0], {'secid': 123, 'secname': 234}))