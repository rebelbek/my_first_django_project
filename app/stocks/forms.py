from django import forms


# from django.core.validators import MinLengthValidator


class SearchForm(forms.Form):
    input = forms.CharField(label='Введите часть названия', max_length=40, required=True)


class DealForm(forms.Form):
    quantity = forms.IntegerField(label='Количество акций', required=False, initial=0)
    buy_price = forms.FloatField(label='Средняя цена 1 акции', required=False, initial=0)
