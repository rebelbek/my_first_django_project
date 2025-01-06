from django.db import models

# Create your models here.

class StockInfo(models.Model):
    secid = models.CharField(max_length=10, unique=True)
    boardid = models.CharField(max_length=40)
    shortname = models.CharField(max_length=40)
    prevprice = models.FloatField()
    lotsize = models.IntegerField()
    facevalue = models.FloatField()
    boardname = models.CharField(max_length=40)
    secname = models.CharField(max_length=40)
    prevwaprice = models.FloatField()
    prevdate = models.DateField()
    issuesize = models.PositiveBigIntegerField()
    isin = models.CharField(max_length=40, primary_key=True)
    latname = models.CharField(max_length=40)
    prevlegalcloseprice = models.FloatField()
    listlevel = models.IntegerField()
    settledate = models.DateField()
    open = models.FloatField(null=True)
    low = models.FloatField(null=True)
    high = models.FloatField(null=True)
    value = models.FloatField(null=True)
    value_usd = models.FloatField(null=True)
    waprice = models.FloatField(null=True)
    valtoday = models.FloatField( null=True)
    valtoday_usd = models.FloatField(null=True)


    def __str__(self):
        return f'Secid = {self.secid} | Shortname = {self.shortname} | Secname = {self.secname} '


    def __eq__(self, other):
        return self.__dict__ == other.__dict__

