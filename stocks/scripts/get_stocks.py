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


def get_data_list(data: list, stocks_fields: list) -> list:
    result = []
    for rows in data['rows']['row']:
        tmp_list = []
        for key, value in rows.items():
            if key[1:].lower() in stocks_fields:
                if not value:
                    tmp_list.append(None)
                elif value.isdigit():
                    tmp_list.append(int(value))
                else:
                    try:
                        tmp_list.append(float(value))
                    except:
                        tmp_list.append(value)
        result.append(tmp_list)
    return result


def get_stocks_list(stocks_fields1: list, stocks_fields2: list) -> list:
    if 'secid' in stocks_fields1:
        zip_result = zip(get_data_list(data_securities, stocks_fields1), get_data_list(data_marketdata, stocks_fields2))
    else:
        zip_result = zip(get_data_list(data_securities, stocks_fields2), get_data_list(data_marketdata, stocks_fields1))
    result = []
    for value1, value2 in zip_result:
        result.append(list(value1 + value2))
    return result
