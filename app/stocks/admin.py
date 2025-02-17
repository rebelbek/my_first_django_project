from django.contrib import admin
from .models import Stocks, CronLogs

# Register your models here.
class StockInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'secid','shortname','secname', 'lotsize', 'issuesize']
    list_per_page = 50
    ordering = ['secid']

class CronLogsAdmin(admin.ModelAdmin):
    list_display = ['func', 'date']
    ordering = ['-date']

admin.site.register(CronLogs, CronLogsAdmin)
admin.site.register(Stocks, StockInfoAdmin)
