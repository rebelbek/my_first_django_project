from django.contrib import admin
from .models import DealInfo, NotificationUser

# Register your models here.

class UserDealAdmin(admin.ModelAdmin):
    list_display = ['id', 'date']
    list_per_page = 20
    ordering = ['date']

class NotificationUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    list_per_page = 20
    ordering = ['id']

admin.site.register(DealInfo, UserDealAdmin)
admin.site.register(NotificationUser, NotificationUserAdmin)