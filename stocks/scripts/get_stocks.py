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


def get_stocks_list():
    list_stocks = []
    for rows in xml_dict['document']['data'][0]['rows']['row']:
        tmp_list = []
        for value in rows.values():
            if value.isdigit():
                tmp_list.append(int(value))
            else:
                try:
                    tmp_list.append(float(value))
                except:
                    tmp_list.append(value)
        list_stocks.append(tmp_list)
    return list_stocks



