from rest_framework.viewsets import ModelViewSet
from .models import Topics
from .serializer import TopicsSerializer

class TopicsViewSet(ModelViewSet):
    queryset = Topics.objects.all()
    serializer_class = TopicsSerializer
