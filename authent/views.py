# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from payments.models import Subscription
from .serializer import (
    UserSignupSerializer,
    ForgotPasswordSerializer, 
    PasswordResetConfirmSerializer,
    VerifyEmailSerializer,
    CustomUserLoginSerializer, 
    TeacherLoginSerializer
)
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode
import logging
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import Teacher

User = get_user_model()
logger = logging.getLogger(__name__)

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User created successfully. Please verify your email."},
                            status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    """
    Handles email verification by checking the token and activating the user.
    """
    def get(self, request, uid, token):
        try:
            user_id = int(urlsafe_base64_decode(uid).decode('utf-8'))
            user = User.objects.get(id=user_id)
            token_generator = PasswordResetTokenGenerator()
            
            # Token validation
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

        # If user is found in CustomUser model
        if user and user.check_password(password):
            # Check if the role matches the user's role
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

            # Role mismatch case
            return Response({"detail": "Invalid role for this user."}, status=status.HTTP_400_BAD_REQUEST)

        # If user is not found in CustomUser, check the Teacher model
        teacher = Teacher.objects.filter(email=email).first()
        if teacher and teacher.check_password(password):
            # Check if the role matches teacher's role
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

            # Role mismatch case
            return Response({"detail": "Invalid role for this user."}, status=status.HTTP_400_BAD_REQUEST)

        # Invalid credentials
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
    permission_classes = [IsAuthenticated]  # Ensure that only authenticated users can access

    def get(self, request):
        user = request.user  # The authenticated user

        # If the user is a school admin and is active
        if user.is_school_admin:
            if not user.is_active:
                return Response({"detail": "School admin account is inactive."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Fetch the subscription status
            subscription = Subscription.objects.filter(user=user).first()
            subscription_status = subscription.is_active if subscription else False
            
            return Response({
                "data": {
                    "role": "school_admin",
                    "name": user.full_name,
                    "email": user.email,
                    "subscription_status": subscription_status,
                }
            }, status=status.HTTP_200_OK)

        # If the user is a teacher (skip is_active check for teachers)
        elif user.is_teacher:
            return Response({
                "data": {
                    "role": "teacher",
                    "name": user.full_name,
                    "email": user.email,
                }
            }, status=status.HTTP_200_OK)

        return Response({"detail": "User is not a teacher or school admin."}, status)