from rest_framework import serializers
from .models import CPD

class CPDModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPD
        fields = ['id', 'title', 'description', 'image']
