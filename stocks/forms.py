from django import forms
from .models import StockInfo

class SearchForm(forms.Form):
    field_choices = [
        ('Secid', 'Тикер'),
        ('Secname', 'Полное название')
    ]
    input = forms.CharField(label='Введите часть названия', max_length=40, required=False)
    field = forms.ChoiceField(label='Выберите поле поиска', widget=forms.RadioSelect, choices=field_choices)

class StockInfoForm(forms.ModelForm):
    class Meta:
        model = StockInfo
        fields = ['shortname', 'secname']
        labels = {
            'shortname' : 'Короткое название',
            'secname' : 'Полное название',
        }
        error_messages = {
            'shortname': {
                'min_lenght': 'Меньше 3 символов',
                'max_lenght': 'Больше 40 символов',
                'required': 'Не должно быть пустым',
            },
            'secname': {
                'min_lenght': 'Меньше 3 символов',
                'max_lenght': 'Больше 40 символов',
                'required': 'Не должно быть пустым',
            }
        }