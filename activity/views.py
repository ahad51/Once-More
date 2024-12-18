from rest_framework.viewsets import ModelViewSet
from .models import Activity
from .serializer import ActivitySerializer

class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
