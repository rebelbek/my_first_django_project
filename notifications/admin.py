from django.contrib import admin
from .models import NotificationUser

# Register your models here.

class NotificationUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    list_per_page = 20
    ordering = ['id']


admin.site.register(NotificationUser, NotificationUserAdmin)