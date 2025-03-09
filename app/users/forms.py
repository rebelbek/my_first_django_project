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
        fields = ['custom_name', 'use_custom', 'quantity', 'buy_price', 'upper_border', 'lower_border']
        labels = {
            'custom_name': 'Название',
            'use_custom': 'Отображать ваше название',
            'quantity': 'Количество акций',
            'buy_price': 'Цена покупки 1 акции',
            'upper_border': 'Верхняя граница для оповещения',
            'lower_border': 'Нижняя граница для оповещения',
        }
        error_messages = {
            'custom_name': {
                'min_length': 'Меньше 3 символов',
                'max_length': 'Больше 40 символов',
                'required': 'Не должно быть пустым',
            },
        }

    def __init__(self, *args, **kwargs):
        super(DealInfoForm, self).__init__(*args, **kwargs)
        self.fields['upper_border'].required = False
        self.fields['lower_border'].required = False


class UserMailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['is_receive_mail']
        labels = {'is_receive_mail': 'Получать оповещения по почте'}
