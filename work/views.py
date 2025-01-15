from rest_framework import viewsets
from .models import HowItWorks
from .serializers import HowItWorksSerializer

class HowItWorksViewSet(viewsets.ModelViewSet):
    queryset = HowItWorks.objects.all()
    serializer_class = HowItWorksSerializer
