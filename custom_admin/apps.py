from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class CustomSectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'custom_admin'  # App name, must match the folder name
    verbose_name = _('Custom Section')  # Name displayed in the Django admin panel
