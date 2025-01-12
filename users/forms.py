from django import forms
from django.core.validators import MinLengthValidator


class DealForm(forms.Form):
    secid = forms.CharField(label='Тикер', max_length=5, validators=[MinLengthValidator(4)], required=True)
    quantity = forms.IntegerField(label='Количество акций', required=True)
    buy_price = forms.FloatField(label='Цена покупки 1 акции', required=True)