from django import forms
from .models import DealInfo, User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    password1 = forms.CharField(required=True, max_length=30, label='Пароль', min_length=8)
    password2 = forms.CharField(required=True, max_length=30, label='Повторите пароль')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')


class AddStocksForm(forms.Form):
    quantity = forms.IntegerField(label='Количество акций')
    buy_price = forms.FloatField(label='Цена покупки 1 акции')


class DealInfoForm(forms.ModelForm):
    class Meta:
        model = DealInfo
        fields = ['custom_name', 'use_custom', 'quantity', 'buy_price']
        labels = {
            'custom_name': 'Название',
            'use_custom': 'Отображать ваше название',
            'quantity': 'Количество акций',
            'buy_price': 'Цена покупки 1 акции',
        }
        error_messages = {
            'custom_name': {
                'min_length': 'Меньше 3 символов',
                'max_length': 'Больше 40 символов',
                'required': 'Не должно быть пустым',
            },
        }


class DealSetBorderForm(forms.ModelForm):
    class Meta:
        model = DealInfo
        fields = ['upper_border', 'lower_border']
        labels = {
            'upper_border': 'Верхняя граница',
            'lower_border': 'Нижняя граница',
        }

    def __init__(self, *args, **kwargs):
        super(DealSetBorderForm, self).__init__(*args, **kwargs)
        self.fields['upper_border'].required = False
        self.fields['lower_border'].required = False