from django.db import models
from tasks.models import Topics  # Original Topics model
from addTasks.models import AddTask  # Original AddTask model
from topicTasks.models import Task  # Original Task model (for AddSubTaskProxy)

# Proxy model for Topics
class TopicsProxy(Topics):
    class Meta:
        proxy = True
        app_label = 'custom_admin'  # You can use 'custom_admin' for app-specific changes
        verbose_name = 'Topics'
        verbose_name_plural = 'Topics'

# Proxy model for AddTask
class AddTaskProxy(AddTask):
    class Meta:
        proxy = True
        app_label = 'custom_admin'  # Custom admin for AddTaskProxy
        verbose_name = 'Add Task'
        verbose_name_plural = 'Add Tasks'

# Proxy model for Task
class AddSubTaskProxy(Task):
    class Meta:
        proxy = True
        app_label = 'custom_admin'  # Custom admin for AddSubTaskProxy
        verbose_name = 'Add Sub Task'
        verbose_name_plural = 'Add Sub Tasks'
