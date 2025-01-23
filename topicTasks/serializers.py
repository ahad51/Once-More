from rest_framework import serializers
from .models import Task
from tasks.models import Topics
from addTasks.models import AddTask

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topics
        fields = ['title']

class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddTask
        fields = ['title']

class TaskSerializer(serializers.ModelSerializer):
    topic = TopicSerializer()
    task = AddTaskSerializer()

    class Meta:
        model = Task
        fields = ['id', 'name', 'description', 'links', 'image', 'downloadable_resources', 'video', 'topic', 'task']  # Added 'video'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return {
            'topic': representation['topic']['title'],
            'task': {
                'title': representation['task']['title'],
                'id': representation['id'],
                'name': representation['name'],
                'description': representation['description'],
                'links': representation['links'],
                'image': representation['image'],
                'downloadable_resources': representation['downloadable_resources'],
                'video': representation['video']  # Added 'video'
            }
        }
