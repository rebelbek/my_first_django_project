from django.contrib import admin
from .models import Stocks

# Register your models here.
class StockInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'secid','shortname','secname', 'lotsize', 'issuesize']
    list_per_page = 50
    ordering = ['secid']

admin.site.register(Stocks, StockInfoAdmin)
