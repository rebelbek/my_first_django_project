from django.db import models
from django.urls import reverse
from django.core.validators import MinLengthValidator

# Create your models here.

class StockInfoSecurities(models.Model):
    secid = models.CharField(max_length=10, unique=True)
    boardid = models.CharField(max_length=40)
    shortname = models.CharField(max_length=20, validators=[MinLengthValidator(3)], blank=False)
    prevprice = models.FloatField()
    lotsize = models.IntegerField()
    facevalue = models.FloatField()
    boardname = models.CharField(max_length=40)
    secname = models.CharField(max_length=40, validators=[MinLengthValidator(3)], blank=False)
    prevwaprice = models.FloatField()
    prevdate = models.DateField()
    issuesize = models.PositiveBigIntegerField()
    isin = models.CharField(max_length=40)
    latname = models.CharField(max_length=40)
    prevlegalcloseprice = models.FloatField()
    listlevel = models.IntegerField()
    settledate = models.DateField()
    unchangeable = models.BooleanField(default=False)
    marketdata = models.OneToOneField('StockInfoMarketdata', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f'{self.secname}'

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_url(self):
        return reverse('stock_detail', args=[self.secid])


class StockInfoMarketdata(models.Model):
    secid = models.CharField(max_length=10, unique=True)
    open = models.FloatField(null=True)
    low = models.FloatField(null=True)
    high = models.FloatField(null=True)
    last = models.FloatField(null=True)
    value = models.FloatField(null=True)
    value_usd = models.FloatField(null=True)
    waprice = models.FloatField(null=True)
    valtoday = models.FloatField(null=True)
    valtoday_usd = models.FloatField(null=True)

    def __str__(self):
        return f'{self.secid}'