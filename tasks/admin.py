# from django.contrib import admin
# from .models import Topics  # Import your model

# @admin.register(Topics)
# class TopicsAdmin(admin.ModelAdmin):
#     list_display = ('title', 'created_at')
#     list_filter = ('title', 'created_at')
#     search_fields = ('title', 'topics')
#     readonly_fields = ('created_at', 'updated_at')
#     def has_module_permission(self, request):
#         # Allow access to the module only for superusers
#         return request.user.is_superuser

#     def has_view_permission(self, request, obj=None):
#         # Allow view permissions only for superusers
#         return request.user.is_superuser
