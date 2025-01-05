from django.db import models


# Create your models here.

class StockInfo(models.Model):
    secid = models.CharField(max_length=10, unique=True)
    boardid = models.CharField(max_length=40)
    shortname = models.CharField(max_length=40)
    prevprice = models.FloatField()
    lotsize = models.IntegerField()
    facevalue = models.FloatField()
    status = models.CharField(max_length=3)
    boardname = models.CharField(max_length=40)
    decimals = models.IntegerField(default=1)
    secname = models.CharField(max_length=40)
    remarks = models.CharField(max_length=40)
    marketcode = models.CharField(max_length=40)
    instrid = models.CharField(max_length=10)
    sectorid = models.CharField(max_length=40)
    minstep = models.FloatField()
    prevwaprice = models.FloatField()
    faceunit = models.CharField(max_length=40)
    prevdate = models.DateField()
    issuesize = models.PositiveBigIntegerField()
    isin = models.CharField(max_length=40, primary_key=True)
    latname = models.CharField(max_length=40)
    regnumber = models.CharField(max_length=40)
    prevlegalcloseprice = models.FloatField()
    currencyid = models.CharField(max_length=40)
    sectype = models.CharField(max_length=40)
    listlevel = models.IntegerField()
    settledate = models.DateField()


    def __str__(self):
        return f'Secid = {self.secid} | Shortname = {self.shortname} | Secname = {self.secname} '


    def __eq__(self, other):
        return self.__dict__ == other.__dict__