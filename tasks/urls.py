from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TopicsViewSet

router = DefaultRouter()
router.register(r'topics', TopicsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
