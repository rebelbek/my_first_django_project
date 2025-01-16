from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from stocks.models import Stocks

# Create your models here.

class DealInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    stock = models.ForeignKey(Stocks, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()
    buy_price = models.IntegerField()
    date = models.DateField()
    upper_border = models.FloatField(default=None, null=True)
    lower_border = models.FloatField(default=None, null=True)
    custom_secname = models.CharField(max_length=40, validators=[MinLengthValidator(3)], blank=False)
    use_custom = models.BooleanField(default=False)

    def __str__(self):
        return self.custom_secname


class NotificationUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    date = models.DateTimeField(default=None, null=True)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'Оповещение для {self.user}, id = {self.id}'