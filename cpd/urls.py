from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CPDModuleViewSet

router = DefaultRouter()
router.register(r'cpd-modules', CPDModuleViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
