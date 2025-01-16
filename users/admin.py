from django.contrib import admin
from .models import DealInfo

# Register your models here.

class UserDealAdmin(admin.ModelAdmin):
    list_display = ['id', 'date']
    list_per_page = 20
    ordering = ['date']

admin.site.register(DealInfo, UserDealAdmin)