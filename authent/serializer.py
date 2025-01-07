import http
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken
from auth.tasks import send_email_verification, send_password_reset_email

User = get_user_model()

from django.conf import settings  # Import settings

class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    is_school_admin = serializers.BooleanField(required=False, default=False)
    is_teacher = serializers.BooleanField(required=False, default=False)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        is_school_admin = validated_data.pop("is_school_admin", False)
        is_teacher = validated_data.pop("is_teacher", False)
        
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data["full_name"],
            is_active=False,  # Account is inactive until email is verified
            is_school_admin=is_school_admin,
            is_teacher=is_teacher
        )
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Dynamically use SITE_URL
        verification_url = f"{settings.SITE_URL}/api/verify-email/{urlsafe_base64_encode(str(user.id).encode())}/{token}/"
        send_email_verification.delay(user.email, verification_url)

        return user


class VerifyEmailSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):
        try:
            user_id = int(urlsafe_base64_decode(data["uid"]).decode("utf-8"))
            user = User.objects.get(id=user_id)

            token_generator = PasswordResetTokenGenerator()
            if token_generator.check_token(user, data["token"]):
                user.is_active = True
                user.save()
                return data
            raise serializers.ValidationError("Invalid or expired token.")
        except Exception:
            raise serializers.ValidationError("Invalid token or user.")


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        
        if not user.is_active:
            raise serializers.ValidationError("Account not verified.")
        
        if not user.check_password(data["password"]):
            raise serializers.ValidationError("Invalid password.")

        # Generate token
        refresh = RefreshToken.for_user(user)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}



class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if not user:
            raise serializers.ValidationError("No user found with this email.")
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)

        # Dynamically use SITE_URL
        reset_url = f"http://localhost:3000/reset-password/{urlsafe_base64_encode(str(user.id).encode())}/{token}/"
        send_password_reset_email.delay(user.email, reset_url, user.full_name)

        return {"message": "Reset email sent"}


class PasswordResetConfirmSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        # Decode the base64 encoded `uid` to get the actual user id
        uid = self.context.get("uid")
        try:
            user_id = int(urlsafe_base64_decode(uid).decode('utf-8'))
        except (TypeError, ValueError, OverflowError):
            raise serializers.ValidationError("Invalid token.")

        token = self.context.get("token")
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise serializers.ValidationError("User not found.")

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Invalid token.")
        
        user.set_password(data["password"])
        user.save()
        return {"message": "Password updated"}
