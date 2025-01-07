from django.contrib import admin
from .models import StockInfoSecurities, StockInfoMarketdata

# Register your models here.
class StockSecuritiesAdmin(admin.ModelAdmin):
    list_display = ['secid','shortname','secname', 'lotsize', 'issuesize']
    list_per_page = 50
    ordering = ['secid']

class StockMarketdataAdmin(admin.ModelAdmin):
    list_display = ['secid']
    list_per_page = 50
    ordering = ['secid']

admin.site.register(StockInfoSecurities, StockSecuritiesAdmin)
admin.site.register(StockInfoMarketdata, StockMarketdataAdmin)