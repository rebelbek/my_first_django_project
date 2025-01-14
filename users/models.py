from django.db import models
from django.core.validators import MinLengthValidator
from stocks.models import Stocks

# Create your models here.

class UserDealInfo(models.Model):
    username = models.CharField(max_length=40)
    secid = models.CharField(max_length=10)
    custom_secname = models.CharField(max_length=40, validators=[MinLengthValidator(3)], blank=False)
    quantity = models.IntegerField()
    buy_price = models.IntegerField()
    date = models.DateField()
    use_custom = models.BooleanField(default=False)
    st = models.ForeignKey(Stocks, on_delete=models.CASCADE, default=None, null=True, blank=True)

    def __str__(self):
        return self.custom_secname