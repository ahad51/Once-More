from rest_framework import viewsets
from .models import Curriculum
from .serializer import CurriculumSerializer

class CurriculumViewSet(viewsets.ModelViewSet):
    queryset = Curriculum.objects.all()
    serializer_class = CurriculumSerializer
