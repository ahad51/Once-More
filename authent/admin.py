from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define the fields to display in the admin list view
    list_display = ("email", "full_name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active", "location", "school_name")
    
    # Fields to search in the admin search bar
    search_fields = ("email", "full_name", "location", "school_name")
    
    # Define fieldsets for the admin detail view
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "location", "school_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    
    # Define fields for the admin add user form
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "full_name", "location", "school_name", "is_active", "is_staff"),
        }),
    )
    
    ordering = ("email",)  # Default ordering in the admin list view

# Register the CustomUser model with the admin panel
admin.site.register(CustomUser, CustomUserAdmin)
