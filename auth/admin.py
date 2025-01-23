from django.contrib.admin import AdminSite

class CustomAdminSite(AdminSite):
    site_header = "Task Management Admin"
    site_title = "Task Management Admin Portal"
    index_title = "Welcome to Task Management"

# Create an instance of the custom admin site
custom_admin_site = CustomAdminSite(name="custom_admin")
