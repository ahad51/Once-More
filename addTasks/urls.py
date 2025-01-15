from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AddTaskViewSet

router = DefaultRouter()
router.register(r'add-taks',AddTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
