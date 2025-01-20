from .models import Stocks
from users.models import DealInfo


def update_stocks():
    Stocks.update_all()


def check_border():
    DealInfo.check_borders()