from django.contrib import admin
from .models import StockInfo

# Register your models here.
class StockAdmin(admin.ModelAdmin):
    list_display = ['secid','shortname','secname', 'lotsize', 'issuesize', 'last']
    list_per_page = 50
    ordering = ['secid']

admin.site.register(StockInfo, StockAdmin)