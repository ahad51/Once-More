from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurriculumViewSet

router = DefaultRouter()
router.register(r'curriculum', CurriculumViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
