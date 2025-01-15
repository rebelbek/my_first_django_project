from django import forms
# from django.core.validators import MinLengthValidator


class SearchForm(forms.Form):
    input = forms.CharField(label='Введите часть названия', max_length=40, required=False)


class DealForm(forms.Form):
    quantity = forms.IntegerField(label='Количество акций', required=True)
    buy_price = forms.FloatField(label='Средняя цена 1 акции', required=True)


# class StockInfoForm(forms.ModelForm):
#     class Meta:
#         model = Stocks
#         fields = ['shortname', 'secname']
#         labels = {
#             'shortname' : 'Короткое название',
#             'secname' : 'Полное название',
#             }
#         error_messages = {
#             'shortname': {
#                 'min_length': 'Меньше 3 символов',
#                 'max_length': 'Больше 40 символов',
#                 'required': 'Не должно быть пустым',
#                 },
#             'secname': {
#                 'min_length': 'Меньше 3 символов',
#                 'max_length': 'Больше 40 символов',
#                 'required': 'Не должно быть пустым',
#                 }
#             }