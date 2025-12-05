from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Customize admin options here, e.g., list_display, search_fields, etc.
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    ordering = ['email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_superuser']
