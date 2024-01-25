from django.contrib import admin
from .models import *


@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'value')


@admin.register(CostCategory)
class CostCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_custom', 'user')
