from django.db import models


# Create your models here.

class StockInfo(models.Model):
    secid = models.CharField(max_length=40, primary_key=True)
    boardid = models.CharField(max_length=40)
    shortname = models.CharField(max_length=40)
    lotsize = models.IntegerField()
    secname = models.CharField(max_length=40)
    listlevel = models.IntegerField()
    issuesize = models.PositiveBigIntegerField()

    def __str__(self):
        return f'Secid = {self.secid} | Shortname = {self.shortname} | Secname = {self.secname} '

    def __eq__(self, other):
        return self.__dict__ == other.__dict__