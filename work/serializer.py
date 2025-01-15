from rest_framework import serializers
from .models import HowItWorks

class HowItWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowItWorks
        fields = ['id', 'title', 'description', 'attachment', 'image']
