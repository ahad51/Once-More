from rest_framework import viewsets
from .models import CPD
from .serializer import CPDModuleSerializer

class CPDModuleViewSet(viewsets.ModelViewSet):
    queryset = CPD.objects.all()
    serializer_class = CPDModuleSerializer
