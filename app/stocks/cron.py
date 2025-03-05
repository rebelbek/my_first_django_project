from .models import Stocks, CronLogs
from users.models import DealInfo


def update_stocks():
    Stocks.update_all()
    DealInfo.check_borders()


def delete_logs():
    CronLogs.objects.all().delete()
