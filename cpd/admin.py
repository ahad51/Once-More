from django.contrib import admin
from .models import CPD

@admin.register(CPD)
class CPDModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'description']
    search_fields = ['title', 'description']
