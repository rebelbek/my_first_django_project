from .views import show_update_logs
from users.models import DealInfo


def update_stocks():
    show_update_logs()


def check_border():
    DealInfo.check_borders()