from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Curriculum, CPDModule, CPDProgress
from .serializer import CurriculumSerializer, CPDModuleSerializer, CPDProgressSerializer

# List of all curriculum
class CurriculumListView(APIView):
    def get(self, request):
        curricula = Curriculum.objects.all()
        serializer = CurriculumSerializer(curricula, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# List of CPD modules
class CPDModuleListView(APIView):
    def get(self, request):
        cpd_modules = CPDModule.objects.all()
        serializer = CPDModuleSerializer(cpd_modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# CPD progress view
class CPDProgressView(APIView):
    def get(self, request):
        progress = CPDProgress.objects.all()
        serializer = CPDProgressSerializer(progress, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# CPD module completion view
class CPDModuleCompletionView(APIView):
    def post(self, request, module_id):
        try:
            cpd_module = CPDModule.objects.get(id=module_id)
            # Logic to mark completion for the given module (e.g., update status)
            cpd_module.completed = True
            cpd_module.save()
            return Response({"message": "Module completion marked."}, status=status.HTTP_200_OK)
        except CPDModule.DoesNotExist:
            return Response({"detail": "Module not found."}, status=status.HTTP_404_NOT_FOUND)
