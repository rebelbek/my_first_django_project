from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from stocks.models import Stocks
from notifications.models import NotificationUser

# Create your models here.

class User(AbstractUser):
    def new_notifications(self):
        notifications = self.notificationuser_set.all()
        for notif in notifications:
            if notif.delivered is False:
                return True
        return False

class DealInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    stock = models.ForeignKey(Stocks, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    buy_price = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    upper_border = models.FloatField(default=None, null=True)
    lower_border = models.FloatField(default=None, null=True)
    custom_secname = models.CharField(max_length=40, validators=[MinLengthValidator(3)], blank=False)
    use_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.custom_secname

    @classmethod
    def check_borders(cls):
        for deal in (cls.objects.filter(upper_border='True') | cls.objects.filter(lower_border='True')):
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