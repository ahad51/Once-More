from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django import forms
from .models import Task
from tasks.models import Topics
from addTasks.models import AddTask

# Custom form for the Task model
class TaskAdminForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('topic', 'task', 'description', 'image', 'downloadable_resources', 'links')

    topic = forms.ModelChoiceField(
        queryset=Topics.objects.all(),
        required=True,
        empty_label="Choose a topic"
    )
    task = forms.ModelChoiceField(
        queryset=AddTask.objects.all(),
        required=True,
        empty_label="Choose a task"
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('topic', 'task', 'description', 'image', 'downloadable_resources', 'links')
    fields = ('topic', 'task', 'description', 'image', 'downloadable_resources', 'links')
    search_fields = ('topic__name', 'task__name')
    list_filter = ('topic', 'task')
    form = TaskAdminForm

    def has_add_permission(self, request):
        if not request.user.is_superuser:
            return False
        return super().has_add_permission(request)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            raise PermissionDenied("Only superusers can add tasks.")
        super().save_model(request, obj, form, change)
