from rest_framework import serializers
from .models import Curriculum, CPDModule, CPDProgress

# Curriculum serializer
class CurriculumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculum
        fields = '__all__'

# CPD Module serializer
class CPDModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPDModule
        fields = '__all__'

# CPD Progress serializer
class CPDProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPDProgress
        fields = '__all__'
