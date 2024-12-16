import logging
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from auth import settings
from .serializer import UserSignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
import requests
from django.utils.http import urlsafe_base64_decode
from .serializer import UserSignupSerializer



User = get_user_model()
logger = logging.getLogger(__name__)

import logging
from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import requests
from auth import settings

User = get_user_model()
logger = logging.getLogger(__name__)

class UserSignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate verification token
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)

            # Create verification URL
            verification_url = request.build_absolute_uri(
                reverse(
                    "email-verify",
                    kwargs={
                        "uid": urlsafe_base64_encode(str(user.id).encode()),
                        "token": token,
                    },
                )
            )

            # Email content
            email_data = {
                "sender": {"email": "ahad51860@gmail.com"},
                "to": [{"email": user.email}],
                "subject": "Email Verification",
                "htmlContent": f"""
                <p>Hello {user.full_name},</p>
                <p>Thank you for signing up. Please verify your email by clicking the link below:</p>
                <a href="{verification_url}">Verify Email</a>
                """,
            }

            # Send email
            try:
                response = requests.post(
                    settings.BREVO_EMAIL_ENDPOINT,
                    headers={"api-key": settings.BRAVO_API_KEY, "Content-Type": "application/json"},
                    json=email_data,
                )

                if response.status_code != 202:
                    logger.error(f"Verification email sending failed: {response.json()}")

            except Exception as e:
                logger.exception("An error occurred while sending verification email.")

            return Response(
                {"message": "User created successfully. Please verify your email."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyEmailView(APIView):
    def get(self, request, uid, token):
        try:
            user_id = int(urlsafe_base64_decode(uid).decode("utf-8"))
            user = User.objects.get(id=user_id)

            token_generator = PasswordResetTokenGenerator()
            if token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                return Response(
                    {"message": "Email verified successfully."},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"error": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response({"error": "Invalid user."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.exception("Error during email verification")
            return Response(
                {"error": "An error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UserLoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response(
                    {"error": "Email not verified. Please verify your email."},
                    status=status.HTTP_403_FORBIDDEN,
                )
            if user.check_password(password):
                from rest_framework_simplejwt.tokens import RefreshToken

                refresh = RefreshToken.for_user(user)
                return Response(
                    {
                        "message": "Login successful",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                    },
                    status=status.HTTP_200_OK,
                )
            raise User.DoesNotExist
        except User.DoesNotExist:
            return Response(
                {"error": "Invalid email or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User with this email does not exist."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Generate password reset token
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Create reset password URL
        reset_url = request.build_absolute_uri(
            reverse('password-reset-confirm', kwargs={'uid': urlsafe_base64_encode(str(user.id).encode()), 'token': token})
        )

        # Email content
        email_data = {
            "sender": {"email": "ahad51860@gmail.com"},
            "to": [{"email": email}],
            "subject": "Password Reset Request",
            "htmlContent": f"<p>Hello {user.full_name},</p>\n <p>You requested a password reset. Click the link below to reset your password:</p>\n                            <a href=\"{reset_url}\">Reset Password</a>\n                            <p>If you did not request this, please ignore this email.</p>"
        }

        # Send email using Brevo API
        try:
            response = requests.post(
                settings.BREVO_EMAIL_ENDPOINT,
                headers={"api-key": settings.BRAVO_API_KEY, "Content-Type": "application/json"},
                json=email_data
            )

            if response.status_code == 202:
                return Response(
                    {"message": "Password reset email sent successfully."},
                    status=status.HTTP_200_OK
                )
            else:
                logger.error(f"Email sending failed: {response.json()}")
                return Response(
                )
        except Exception as e:
            logger.exception("An error occurred while sending password reset email.")
            return Response(
                {"error": "An internal error occurred. Please try again later."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PasswordResetConfirmView(APIView):
    def post(self, request, uid, token):
        try:
            user_id = int(urlsafe_base64_decode(uid).decode('utf-8'))
            
            # Get the user
            user = User.objects.get(id=user_id)

            # Check if the token is valid
            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                return Response(
                    {"error": "Invalid or expired token."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            new_password = request.data.get("password")
            if not new_password:
                return Response(
                    {"error": "New password is required."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()

            return Response(
                {"message": "Password has been reset successfully."},
                status=status.HTTP_200_OK
            )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.exception("Error resetting password")
            return Response(
                {"error": "An error occurred. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
