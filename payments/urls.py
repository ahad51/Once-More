from django.urls import path
from .views import SubscriptionView

urlpatterns = [
    path('subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('update-subscription/', SubscriptionView.as_view(), name='update_subscription'),
    path('cancel-subscription/', SubscriptionView.as_view(), name='cancel_subscription'),
]
