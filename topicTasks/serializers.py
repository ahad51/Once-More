from rest_framework import serializers
from .models import Task
from tasks.models import Topics
from addTasks.models import AddTask

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['title']  # Changed from 'name' to 'title'

class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddTask
        fields = ['title']  # Changed from 'name' to 'title'

class TaskSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()  # Nested TopicSerializer for the topic title
    task = AddTaskSerializer()  # Nested AddTaskSerializer for the task title

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'links', 'image', 'downloadable_resources', 'topic', 'task']

    def to_representation(self, instance):
        # Get the default representation
        representation = super().to_representation(instance)
        
        # Structure the output as per your requirement
        return {
            'topic': representation['topic']['title'],  # Just topic title
            'task': {
                'title': representation['task']['title'],  # Task title
                'id': representation['id'],  # Task ID
                'name': representation['name'],  # Task name
                'description': representation['description'],
                'links': representation['links'],
                'image': representation['image'],
                'downloadable_resources': representation['downloadable_resources']
            }
        }
