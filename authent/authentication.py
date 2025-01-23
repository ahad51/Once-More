from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from .models import Teacher

class TeacherAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # First, check if a teacher exists with the provided username (email)
            teacher = Teacher.objects.get(email=username)

            # Check the provided password
            if teacher.check_password(password):
                # Return the associated CustomUser instance
                return teacher.user
        except Teacher.DoesNotExist:
            # If the teacher doesn't exist, return None
            return None
        except ObjectDoesNotExist:
            # If there's an issue with the object retrieval
            return None


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)  # Get user from token
        
        # Skip 'is_active' check for teachers
        if user.is_teacher:
            return user
        
        # Check if user is active for others (e.g., school admins)
        if not user.is_active:
            raise AuthenticationFailed('User is inactive')
        
        return user
