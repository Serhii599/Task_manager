from django.contrib import admin
from .models import *


@admin.register(Task)
class TaskInfoAdmin(admin.ModelAdmin):
    # Customize admin options here, e.g., list_display, search_fields, etc.
    pass

@admin.register(Project)
class ProjectsAdmin(admin.ModelAdmin):
    # Customize admin options here, e.g., list_display, search_fields, etc.
    pass