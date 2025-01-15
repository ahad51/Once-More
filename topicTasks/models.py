from django.db import models
from tasks.models import Topics  # Assuming Topics is in the tasks app
from addTasks.models import AddTask

class Task(models.Model):
    topic = models.ForeignKey(Topics, on_delete=models.CASCADE)
    task = models.ForeignKey(AddTask, on_delete=models.CASCADE ,default=1)
    name = models.CharField(max_length=255, default='Untitled')
    description = models.TextField(default='Default description text', blank=True, null=True)
    links = models.TextField(default='links', blank=True, null=True)
    image = models.ImageField(upload_to='activities/images/', blank=True, null=True)
    downloadable_resources = models.FileField(upload_to='activities/resources/', blank=True, null=True)

    def __str__(self):
        return self.name

    @staticmethod
    def get_initial_tasks():
        return [
            {'topic': 'Engineer Role Model', 'name': 'Engineer Role Model'},
            {'topic': 'Explainer', 'name': 'Explainer'},
            {'topic': 'Activity 1', 'name': 'Activity 1'},
            {'topic': 'Activity 2', 'name': 'Activity 2'},
            {'topic': 'Activity 3', 'name': 'Activity 3'},
            {'topic': 'Story', 'name': 'Story'},
            {'topic': 'Objectives', 'name': 'Objectives'},
            {'topic': 'Junk Modelling', 'name': 'Junk Modelling'},
            {'topic': 'Play Provocations', 'name': 'Play Provocations'},
            {'topic': 'Physical Activities', 'name': 'Physical Activities'},
            {'topic': 'Games', 'name': 'Games'},
            {'topic': 'Extensions', 'name': 'Extensions'},
        ]
