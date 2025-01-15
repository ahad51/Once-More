from rest_framework.viewsets import ModelViewSet
from .models import AddTask
from .serializer import AddTaskSerializer

class AddTaskViewSet(ModelViewSet):
    queryset = AddTask.objects.all()
    serializer_class = AddTaskSerializer
