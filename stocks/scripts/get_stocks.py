import os
import sys
import requests # внешний модуль
from bs4 import BeautifulSoup # внешний модуль
# дополнительно должен быть установлен модуль lxml (он нужен для BeautifulSoup)

# добавил путь для импорта скрипта который получает url из .env
# и импортировал переменную из скрипта
sys.path.append(os.path.join(os.getcwd(), '../..'))
from env.get_from_env import url_from_env

url = url_from_env

response = requests.get(url)
soup = BeautifulSoup(response.content, 'xml')

# для выборки полей из данных xml
list_names = ['secid', 'boardid', 'shortname', 'lotsize', 'secname', 'listlevel', 'issuesize']
data = None

for i in soup.find_all('data'):
    if i['id'] == 'securities':
        data = i
        break

rows = data.select('row')


def get_stocks_list() -> list:
    stocks_list = []
    for row in rows:
        tmp_dict = {}  # для временного хранения значений из одной строки row
        for item in list_names:
            if row[item.upper()].isdigit():
                tmp_dict[item] = int(row[item.upper()])
            else:
                tmp_dict[item] = row[item.upper()]
        stocks_list.append(tmp_dict)
    return stocks_list


def show_stocks_list() -> None:
    stocks_list = get_stocks_list()
    for item in stocks_list:
        tmp_list = []
        for key, value in item.items():
            tmp_list.append(f'{key.title()} = {value}')
        print(' | '.join(tmp_list))
        print('-' * 130)

# если открывается из самого скрипта без импортирования
if __name__ == "__main__":
    show_stocks_list()


