from django.contrib import admin
from .models import UserDealInfo

# Register your models here.

class UserDealAdmin(admin.ModelAdmin):
    list_display = ['secid']
    list_per_page = 20
    ordering = ['date']

admin.site.register(UserDealInfo, UserDealAdmin)