import os
import sys
import requests # внешний модуль
import xmltodict # внешний модуль

# добавил путь для импорта скрипта который получает url из .env
# и импортировал переменные из скрипта
sys.path.append(os.path.join(os.getcwd(), '../..'))
from env.get_from_env import url_stocks, url_stock


def get_data(url) -> list[dict]:
    response = requests.get(url)
    xml = response.content
    xml_dict = xmltodict.parse(xml)
    data_securities = xml_dict['document']['data'][0]
    data_marketdata = xml_dict['document']['data'][1]
    data = [data_securities, data_marketdata]
    return data


def get_data_for_all(data: dict, stocks_fields: list) -> list[dict]:
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


def get_data_for_one(data: dict, stock_fields: dict) -> dict:
     result = {}
     for key, value in data['rows']['row'].items():
         if key[1:].lower() in stock_fields:
             if not value:
                 result[key[1:].lower()] = None
             elif value.isdigit():
                 result[key[1:].lower()] = int(value)
             else:
                 try:
                     result[key[1:].lower()] = float(value)
                 except:
                     result[key[1:].lower()] = value
     return result


def get_stocks_dict(stocks_fields: list) -> list:
    data = get_data(url_stocks)
    result1 = get_data_for_all(data[0], stocks_fields)
    result2 = get_data_for_all(data[1], stocks_fields)
    result = [{**values1, **values2} for values1, values2 in zip(result1, result2)]
    return result


def get_stock_dict(stock_fields: dict) -> dict:
    url = url_stock.replace('{BOARDID}', stock_fields['boardid']).replace('{TICKER}', stock_fields['secid'])
    data = get_data(url)
    result1 = get_data_for_one(data[0], stock_fields)
    result2 = get_data_for_one(data[1], stock_fields)
    result = {**result1, **result2}
    return result

# для проверок
if __name__ == '__main__':
    lst = get_data(url_stock.replace('{BOARDID}', 'TQBR').replace('{TICKER}', 'ABIO'))
    print(lst[0]['rows']['row'])
    print(get_data_for_one(lst[0], {'secid': 123, 'secname': 234}))