from django import forms
from .models import StockInfoSecurities


class SearchForm(forms.Form):
    field_choices = [
        ('Secid', 'Тикер'),
        ('Secname', 'Полное название')
    ]
    input = forms.CharField(label='Введите часть названия', max_length=40, required=False)
    field = forms.ChoiceField(label='Выберите поле поиска', widget=forms.RadioSelect, choices=field_choices)


class StockInfoForm(forms.ModelForm):
    class Meta:
        model = StockInfoSecurities
        fields = ['shortname', 'secname', 'unchangeable']
        labels = {
            'shortname' : 'Короткое название',
            'secname' : 'Полное название',
            'unchangeable' : 'Не изменять при обновлении',
            }
        error_messages = {
            'shortname': {
                'min_length': 'Меньше 3 символов',
                'max_length': 'Больше 40 символов',
                'required': 'Не должно быть пустым',
                },
            'secname': {
                'min_length': 'Меньше 3 символов',
                'max_length': 'Больше 40 символов',
                'required': 'Не должно быть пустым',
                }
            }