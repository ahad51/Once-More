from django.contrib import admin
from django import forms
from .models import TopicsProxy, AddTaskProxy, AddSubTaskProxy  # Import the proxy models

# Custom form for TopicsProxy
class TopicsProxyAdminForm(forms.ModelForm):
    class Meta:
        model = TopicsProxy
        fields = '__all__'

# Admin configuration for TopicsProxy
@admin.register(TopicsProxy)
class TopicsProxyAdmin(admin.ModelAdmin):
    form = TopicsProxyAdminForm
    list_display = ('title',)
    search_fields = ('title',)
    list_filter = ('title',)


# Custom form for AddTaskProxy
class AddTaskProxyAdminForm(forms.ModelForm):
    class Meta:
        model = AddTaskProxy
        fields = '__all__'  # Use '__all__' to inherit fields from the AddTask model

# Admin configuration for AddTaskProxy
@admin.register(AddTaskProxy)
class AddTaskProxyAdmin(admin.ModelAdmin):
    form = AddTaskProxyAdminForm  # Use the custom form

    # Ensure 'name' is valid - Either the field exists, or create a method
    def get_task_name(self, obj):
        return obj.task_name  # If 'task_name' is the correct field in the AddTask model

    get_task_name.short_description = 'Task Name'  # Optional: customize column header
    
    list_display = ('get_task_name',)  # Display the 'get_task_name' method in the admin list view
    search_fields = ('task_name',)  # Allow searching by the 'task_name' field


# Custom form for AddSubTaskProxy
class AddSubTaskProxyAdminForm(forms.ModelForm):
    class Meta:
        model = AddSubTaskProxy
        fields = '__all__'  # Use '__all__' to inherit fields from the Task model

# Admin configuration for AddSubTaskProxy
@admin.register(AddSubTaskProxy)
class AddSubTaskProxyAdmin(admin.ModelAdmin):
    form = AddSubTaskProxyAdminForm  # Use the custom form
    list_display = ('name', 'topic', 'task')  # Display relevant fields in the admin list view
    search_fields = ('name', 'topic__name', 'task__name')  # Allow searching by 'name', 'topic', and 'task'
    list_filter = ('topic', 'task')  # Filter by 'topic' and 'task'
