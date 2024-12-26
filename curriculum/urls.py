from django.urls import path
from . import views

urlpatterns = [
    path('curriculum/', views.CurriculumListView.as_view(), name='curriculum-list'),
    path('cpd-modules/', views.CPDModuleListView.as_view(), name='cpd-module-list'),
    path('cpd-progress/', views.CPDProgressView.as_view(), name='cpd-progress'),
    path('cpd-progress/completion/<int:module_id>/', views.CPDModuleCompletionView.as_view(), name='cpd-module-completion'),
]
