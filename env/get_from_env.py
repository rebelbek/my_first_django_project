import os
from dotenv import load_dotenv # внешний модуль python-dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

def get_url_from_env():
    # функция получает url из файла .env и отдает его
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    return os.environ.get('url')

def get_db_passw_from_env():
    # функция получает password для db из файла .env и отдает его
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    return os.environ.get('db_conf_passw')

def get_db_user_from_env():
    # функция получает user для db из файла .env и отдает его
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)
    return os.environ.get('db_conf_user')
