from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CustomAdminSectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'addTasks'  # Keep the actual app name here
    verbose_name = _('Topic/Tasks')  # The name you want to display in the admin panel
