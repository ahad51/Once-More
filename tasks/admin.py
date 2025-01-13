from django.contrib import admin
from .models import Task  # Import your model

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'category')
    readonly_fields = ('created_at', 'updated_at')
    def has_module_permission(self, request):
        # Allow access to the module only for superusers
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        # Allow view permissions only for superusers
        return request.user.is_superuser
