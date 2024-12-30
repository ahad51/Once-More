from rest_framework.permissions import BasePermission

class IsActiveSubscriber(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.subscription.is_active
