import os
from dotenv import load_dotenv # внешний модуль python-dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

url_stocks = os.environ.get('url_stocks')
url_stock = os.environ.get('url_stock')
db_name = os.environ.get('db_name')
db_user = os.environ.get('db_user')
db_password = os.environ.get('db_passw')

