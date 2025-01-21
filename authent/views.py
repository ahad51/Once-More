# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
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
        role = request.data.get("role")  # Optional: for frontend role checking

        # Debugging step: Log incoming data
        print(f"Email: {email}, Password: {password}, Role: {role}")

        # Try to find a CustomUser first
        user = User.objects.filter(email=email).first()

        if user:
            # Check if the password is correct for CustomUser
            if user.check_password(password):  # Password validation for CustomUser
                print(f"CustomUser {email} logged in successfully.")  # Debug log
                if role == 'teacher' and user.is_teacher:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "message": "Teacher logged in successfully",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    }, status=status.HTTP_200_OK)
                elif role == 'school_admin' and user.is_school_admin:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "message": "School Admin logged in successfully",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({"detail": "Invalid role for this user."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                print("CustomUser password mismatch.")
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        # If no CustomUser, check if Teacher exists
        teacher = Teacher.objects.filter(email=email).first()

        if teacher:
            # Check if the password is correct for Teacher
            if teacher.check_password(password):  # Password validation for Teacher
                print(f"Teacher {email} logged in successfully.")  # Debug log
                refresh = RefreshToken.for_user(teacher)
                return Response({
                    "message": "Teacher logged in successfully",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                print("Teacher password mismatch.")
                return Response({"detail": "Invalid credentials."}, status=status.HTTP_400_BAD_REQUEST)

        # If neither user nor teacher exists, return error
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
