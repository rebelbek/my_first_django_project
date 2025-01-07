import os
from dotenv import load_dotenv # внешний модуль python-dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
url_from_env = os.environ.get('url')
db_password = os.environ.get('db_conf_passw')
db_user = os.environ.get('db_conf_user')