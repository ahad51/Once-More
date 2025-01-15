from django.contrib import admin
from .models import HowItWorks

@admin.register(HowItWorks)
class HowItWorksAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'attachment', 'image']
    search_fields = ['title', 'description']
    list_filter = ['title']
