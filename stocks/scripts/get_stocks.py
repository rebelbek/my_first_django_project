import os
import sys
import requests # внешний модуль
import xmltodict # внешний модуль

# добавил путь для импорта скрипта который получает url из .env
# и импортировал переменную из скрипта
sys.path.append(os.path.join(os.getcwd(), '../..'))
from env.get_from_env import url_from_env

try:
    url = url_from_env
    response = requests.get(url)
    xml = response.content
    xml_dict = xmltodict.parse(xml)
    data_securities = xml_dict['document']['data'][0]
    data_marketdata = xml_dict['document']['data'][1]
except:
    pass


def get_data_list(data: list, stocks_fields: dict) -> dict:
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


def get_stocks_list(stocks_fields: dict) -> dict:
    if 'secname' in stocks_fields:
        result = get_data_list(data_securities, stocks_fields)
    else:
        result = get_data_list(data_marketdata, stocks_fields)
    return result
