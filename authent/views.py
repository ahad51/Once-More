from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from payments.models import Subscription
from .models import Teacher
from .serializer import (
    UserSignupSerializer,
    ForgotPasswordSerializer, 
    PasswordResetConfirmSerializer,
    VerifyEmailSerializer,
    CustomUserLoginSerializer, 
    TeacherLoginSerializer
)

User = get_user_model()
logger = logging.getLogger(__name__)

# Custom authentication backend for teachers
class TeacherAuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # First, check if a teacher exists with the provided username (email)
            teacher = Teacher.objects.get(email=username)

            # Check the provided password
            if teacher.check_password(password):
                return teacher.user  # Return the associated CustomUser instance
        except Teacher.DoesNotExist:
            return None
        except ObjectDoesNotExist:
            return None

# Custom JWT Authentication Class to allow inactive teachers
class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        user = super().get_user(validated_token)

        # Skip 'is_active' check for teachers
        if hasattr(user, "is_teacher") and user.is_teacher:
            return user  # Allow inactive teachers

        # If not a teacher, check if user is active
        if not user.is_active:
            raise AuthenticationFailed({"detail": "User is inactive", "code": "user_inactive"})

        return user

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully. Please verify your email."},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyEmailView(APIView):
    def get(self, request, uid, token):
        try:
            user_id = int(urlsafe_base64_decode(uid).decode('utf-8'))
            user = User.objects.get(id=user_id)
            token_generator = PasswordResetTokenGenerator()
            
            if token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
            return Response({"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Invalid user."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error("Error during email verification", exc_info=True)
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role")  # Expected role from the frontend

        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            if role == "school_admin" and user.is_school_admin:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "data": {
                        "id": user.id,
                        "name": user.full_name,
                        "email": user.email,
                        "role": "school_admin",
                    }
                }, status=status.HTTP_200_OK)

            elif role == "teacher" and user.is_teacher:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "data": {
                        "id": user.id,
                        "name": user.full_name,
                        "email": user.email,
                        "role": "teacher",
                    }
                }, status=status.HTTP_200_OK)

            return Response({"detail": "Invalid role for this user."}, status=status.HTTP_400_BAD_REQUEST)

        # If user is not found in CustomUser, check the Teacher model
        teacher = Teacher.objects.filter(email=email).first()
        if teacher and teacher.check_password(password):
            if role == "teacher":
                refresh = RefreshToken.for_user(teacher)
                return Response({
                    "message": "Login successful",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "data": {
                        "id": teacher.id,
                        "name": teacher.full_name,
                        "email": teacher.email,
                        "role": "teacher",
                    }
                }, status=status.HTTP_200_OK)

            return Response({"detail": "Invalid role for this user."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid():
            return Response({"message": "Password reset email sent successfully."},
                            status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        serializer = PasswordResetConfirmSerializer(
            data=request.data, context={"uid": uid, "token": token}
        )
        if serializer.is_valid():
            return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [CustomJWTAuthentication]  

    def get(self, request):
        user = request.user  

        if user.is_school_admin:
            if not user.is_active:
                return Response({"detail": "School admin account is inactive."}, status=status.HTTP_400_BAD_REQUEST)

            subscription = Subscription.objects.filter(user=user).first()
            subscription_status = subscription.is_active if subscription else False
            subscription_id = subscription.stripe_subscription_id if subscription else None

            return Response({
                "data": {
                    "role": "school_admin",
                    "name": user.full_name,
                    "email": user.email,
                    "subscription_status": subscription_status,
                    "subscription_id": subscription_id,
                }
            }, status=status.HTTP_200_OK)

        if user.is_teacher:
            return Response({
                "data": {
                    "role": "teacher",
                    "name": user.full_name,
                    "email": user.email,
                }
            }, status=status.HTTP_200_OK)

        return Response({"detail": "User is not a teacher or school admin."}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
        permission_classes = [IsAuthenticated]

        def post(self, request):
            current_password = request.data.get("current_password")
            new_password = request.data.get("new_password")
            
            # Get the authenticated user
            user = request.user

            # Validate current password
            if not user.check_password(current_password):
                return Response({"detail": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            # Set the new password
            user.set_password(new_password)
            user.save()

            return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)