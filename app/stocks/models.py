from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.core.validators import MinLengthValidator
from .scripts.get_stocks import get_stocks_dict, get_stock_dict


# Create your models here.

class CronLogs(models.Model):
    func = models.CharField(max_length=40)
    date = models.DateTimeField(default=timezone.now())

    class Meta:
        ordering = ['-date']


class Stocks(models.Model):
    secid = models.CharField(max_length=10, unique=True)
    boardid = models.CharField(max_length=40)
    shortname = models.CharField(max_length=20, validators=[MinLengthValidator(3)], blank=False)
    prevprice = models.FloatField(null=True)
    lotsize = models.IntegerField()
    facevalue = models.FloatField()
    boardname = models.CharField(max_length=40)
    secname = models.CharField(max_length=40, validators=[MinLengthValidator(3)], blank=False)
    prevwaprice = models.FloatField(null=True)
    # prevdate = models.DateField()
    issuesize = models.PositiveBigIntegerField()
    isin = models.CharField(max_length=40)
    latname = models.CharField(max_length=40)
    prevlegalcloseprice = models.FloatField(null=True)
    listlevel = models.IntegerField()
    # settledate = models.DateField()
    open = models.FloatField(null=True)
    low = models.FloatField(null=True)
    high = models.FloatField(null=True)
    last = models.FloatField(null=True)
    value = models.FloatField(null=True)
    value_usd = models.FloatField(null=True)
    waprice = models.FloatField(null=True)
    valtoday = models.FloatField(null=True)
    valtoday_usd = models.FloatField(null=True)

    class Meta:
        ordering = ['secid']

    def __str__(self):
        return f'{self.secname}'

    def get_url(self):
        return reverse('stock_detail', args=[self.secid])

    @classmethod
    def download(cls):
        stocks_fields = get_stocks_dict(list(cls.__dict__.keys()))
        cls.objects.bulk_create(cls(**item) for item in stocks_fields)

    @classmethod
    def update_all(cls):
        CronLogs.objects.create(func='stocks_update')
        stocks_fields = get_stocks_dict(list(cls.__dict__.keys()))
        for item in stocks_fields:
            cls.objects.update_or_create(secid=item['secid'], defaults=item)

    @classmethod
    def update_one(cls, secid):
        stock_fields = get_stock_dict(dict(cls.objects.get(secid=secid).__dict__.items()))
        cls.objects.filter(secid=secid).update(**stock_fields)

# python3 manage.py shell_plus --print-sql
