from django.contrib import admin
from .models import CostCategory, Cost


@admin.register(Cost)
class CostAdmin(admin.ModelAdmin):
    """ Переопределение отображения модели Cost в админке """
    list_display = ('pk', 'user', 'category', 'value', 'date')


@admin.register(CostCategory)
class CostCategoryAdmin(admin.ModelAdmin):
    """ Переопределение отображения модели CostCategory в админке """
    list_display = ('pk', 'name', 'is_custom', 'user')
