from django import forms
from.models import UserDealInfo


# class DealForm(forms.Form):
#     secid = forms.CharField(label='Тикер', max_length=5, validators=[MinLengthValidator(4)], required=True)
#     quantity = forms.IntegerField(label='Количество акций', required=True)
#     buy_price = forms.FloatField(label='Средняя цена 1 акции', required=True)


class AddStocksForm(forms.Form):
    quantity = forms.IntegerField(label='Количество акций')
    buy_price = forms.FloatField(label='Средняя цена покупки')


class DealInfoForm(forms.ModelForm):
    class Meta:
        model = UserDealInfo
        fields = ['custom_secname', 'use_custom', 'quantity', 'buy_price']
        labels = {
            'custom_secname' : 'Название',
            'use_custom' : 'Отображать ваше название',
            'quantity' : 'Количество акций',
            'buy_price' : 'Цена покупки 1 акции',
            }
        error_messages = {
            'custom_secname': {
                'min_length': 'Меньше 3 символов',
                'max_length': 'Больше 40 символов',
                'required': 'Не должно быть пустым',
                },
            }



