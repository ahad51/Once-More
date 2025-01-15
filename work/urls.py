from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HowItWorksViewSet

router = DefaultRouter()
router.register(r'howitworks', HowItWorksViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
