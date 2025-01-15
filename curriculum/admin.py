from django.contrib import admin
from .models import Curriculum

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ['title', 'link', 'description', 'image']
    search_fields = ['title', 'description']
    list_filter = ['title']
