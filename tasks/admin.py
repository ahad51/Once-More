from django.contrib import admin
from .models import Task  # Import your model

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'category')
    readonly_fields = ('created_at', 'updated_at')
