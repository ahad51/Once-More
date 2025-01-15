from rest_framework import serializers
from .models import AddTask

class AddTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddTask
        fields = '__all__'
