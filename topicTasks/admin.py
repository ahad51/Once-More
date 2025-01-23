# from django.contrib import admin
# from django.core.exceptions import PermissionDenied
# from django import forms
# from .models import Task
# from tasks.models import Topics  # Assuming Topics is in the tasks app
# from addTasks.models import AddTask

# # Custom form for the Task model
# class TaskAdminForm(forms.ModelForm):
#     class Meta:
#         model = Task
#         fields = ('name', 'topic', 'task', 'description', 'image', 'downloadable_resources', 'links','video')

#     # ModelChoiceField for selecting topics from the Topics model
#     topic = forms.ModelChoiceField(
#         queryset=Topics.objects.all(), 
#         required=True, 
#         empty_label="Choose a topic"
#     )

#     # ModelChoiceField for selecting tasks from the AddTask model
#     task = forms.ModelChoiceField(
#         queryset=AddTask.objects.all(), 
#         required=True, 
#         empty_label="Choose a task"
#     )

#     # Custom save method
#     def save(self, commit=True):
#         instance = super().save(commit=False)
#         if instance.topic is None:
#             # Create a new topic if the user selects the "Create New Topic" option
#             new_topic = Topics.objects.create(name=self.cleaned_data['name'])
#             instance.topic = new_topic
#         if commit:
#             instance.save()
#         return instance

# @admin.register(Task)
# class TaskAdmin(admin.ModelAdmin):
#     list_display = ('name', 'topic', 'task', 'description', 'image', 'downloadable_resources', 'links','video')
#     fields = ('name', 'topic', 'task', 'description', 'image', 'downloadable_resources', 'links','video')
#     search_fields = ('name', 'topic__name', 'task__name')
#     list_filter = ('topic', 'task')
#     form = TaskAdminForm  # Use the custom form

#     # Restrict permissions for adding tasks (only superusers can add tasks)
#     def has_add_permission(self, request):
#         if not request.user.is_superuser:
#             return False
#         return super().has_add_permission(request)

#     def save_model(self, request, obj, form, change):
#         if not request.user.is_superuser:
#             raise PermissionDenied("Only superusers can add tasks.")
#         super().save_model(request, obj, form, change)
