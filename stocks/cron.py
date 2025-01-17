from .models import Stocks
from users.models import DealInfo
from notifications.models import NotificationUser
from .scripts.get_stocks import get_stocks_dict


def update_stocks():
    stocks_fields = get_stocks_dict(list(Stocks().__dict__.keys()))
    for item in stocks_fields:
        try:
            Stocks.objects.filter(secid=item['secid']).update(**item)
        except:
            Stocks.objects.create(**item)


def check_border():
    for deal in DealInfo.objects.all():
        if deal.upper_border:
            if deal.stock.last >= deal.upper_border:
                notification = NotificationUser(user=deal.user,
                                                text=f'Достигнута верхняя граница {deal.upper_border} для позиции {deal.custom_secname}')
                deal.upper_border = None
                deal.save()
                notification.save()
        if deal.lower_border:
            if deal.stock.last <= deal.lower_border:
                notification = NotificationUser(user=deal.user,
                                                text=f'Достигнута нижняя граница {deal.lower_border} для позиции {deal.custom_secname}')
                deal.lower_border = None
                deal.save()
                notification.save()