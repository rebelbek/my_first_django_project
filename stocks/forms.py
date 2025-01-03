from random import choices

from django import forms

class SearchForm(forms.Form):
    field_choices = [
        ('Secid', 'Secid'),
        ('Secname', 'Secname')
    ]
    input = forms.CharField(label='Введите часть названия', max_length=40, required=False)
    field = forms.ChoiceField(label='Выберите поле поиска', widget=forms.RadioSelect, choices=field_choices)
