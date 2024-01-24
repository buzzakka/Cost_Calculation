from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'date_joined')
    fields = ('email', 'username', 'date_joined', 'image', 'groups')
    search_fields = ('email', 'username')
