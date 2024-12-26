from django.contrib import admin
from .models import Curriculum, CPDModule, CPDProgress

@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']


@admin.register(CPDModule)
class CPDModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_completed', 'completion_date')
    search_fields = ['title']


@admin.register(CPDProgress)
class CPDProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'module', 'progress')
    search_fields = ['user__username', 'module__title']
