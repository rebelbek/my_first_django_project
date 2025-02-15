from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import DealInfo, User

# Register your models here.

class CustomUserAdmin(UserAdmin):
    pass

class UserDealAdmin(admin.ModelAdmin):
    list_display = ['id', 'date']
    list_per_page = 20
    ordering = ['date']


admin.site.register(DealInfo, UserDealAdmin)
admin.site.register(User, CustomUserAdmin)
