# Проект py_dd

В проекте содержится приложение stocks, которое получает
данные с мосбиржи, сохраняет их в базу данных и отображает в html.

## Необходимые модули для установки:

* django
* django-extensions
* requests
* xmltodict
* python-dotenv
* psycopg2-binary

В проекте используется база данных ***PostgreSQl***, её нужно установить 
в вашей системе или вы можете использовать встроенный в django ***SQLite***.

## Настройка

Создайте файл **.env** в папке **env** которая находится в корне проекта
**py_dd** и добавить следующие настройки:

```
url = https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.xml
db_name = имя_вашей_базы_данных
db_user = имя_пользователя
db_passw = пароль_от_базы_данных
```

Если вы используете ***SQLite*** в качестве базы данных, то вам
нужно изменить переменную **DATABASE** в файле **settings.py**, 
которая находится в папке py_dd на следующее:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

И можно удалить часть кода в начале файла ***settings.py***:

```python
import os
import sys

# добавить путь для импорта скрипта который получает данные из .env
# и импортировать переменные из скрипта
sys.path.append(os.path.join(os.getcwd(), '..'))
from env.get_from_env import db_name, db_user, db_password
```

## Запуск

После установки необходимых модулей и настройки работы с базой данных
в терминале перейдите в корневой каталог проекта **py_dd** и выполните миграцию
для создания таблиц в базе данных:

`python3 manage.py migrate` - у вас может быть просто python или совсем без него.

Можно запускать сервер:

`python3 manage.py runserver`