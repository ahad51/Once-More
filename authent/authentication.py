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
