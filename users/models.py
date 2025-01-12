from django.db import models
from django.forms import CharField
from stocks.models import StockInfoSecurities

# Create your models here.

class UserDealInfo(models.Model):
    stock = models.ForeignKey(StockInfoSecurities, on_delete=models.SET_NULL, null = True)
    username = models.CharField(max_length=40)
    secid = models.CharField(max_length=10)
    quantity = models.IntegerField()
    buy_price = models.IntegerField()
    date = models.DateField()