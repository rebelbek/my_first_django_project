from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import DjangoInfo, DjangoLink, DjangoImage

# # Register your models here.

admin.site.register(DjangoLink)
admin.site.register(DjangoImage)

class StudyAdmin(admin.ModelAdmin):
    list_display = ['chapter_name', 'number']
    list_editable = ['number']
    list_per_page = 50
    filter_horizontal = ['links']
    ordering = ['number']
    search_fields = ['chapter_name__iregex'] #__iregex для игнорирования регистра букв в кириллице
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':40, 'cols': 100})},
    }

admin.site.register(DjangoInfo, StudyAdmin)