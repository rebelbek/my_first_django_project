import os
from dotenv import load_dotenv # внешний модуль python-dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
url_from_env = os.environ.get('url')
db_name = os.environ.get('db_name')
db_user = os.environ.get('db_user')
db_password = os.environ.get('db_passw')

