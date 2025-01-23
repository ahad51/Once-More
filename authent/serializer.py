# serializers.py
from django.conf import settings
from django.db import IntegrityError
from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken
from auth.tasks import send_email_verification, send_password_reset_email
from authent.models import Teacher
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()

class UserSignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField()
    is_school_admin = serializers.BooleanField(required=False, default=False)
    is_teacher = serializers.BooleanField(required=False, default=False)

    def validate(self, data):
        # Ensure that the user is either a school admin or a teacher, not both
        if data.get('is_school_admin') and data.get('is_teacher'):
            raise serializers.ValidationError("User cannot be both a school admin and a teacher.")
        return data

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def create(self, validated_data):
        is_school_admin = validated_data.pop("is_school_admin", False)
        is_teacher = validated_data.pop("is_teacher", False)

        if is_teacher:
            # Teacher should be created as an active user
            is_active = True
        else:
            # Set inactive only for CustomUser (non-teachers)
            is_active = False

        try:
            user = User.objects.create_user(
                email=validated_data["email"],
                password=validated_data["password"],
                full_name=validated_data["full_name"],
                is_active=is_active,  # Account is inactive for CustomUser, active for Teacher
                is_school_admin=is_school_admin,
                is_teacher=is_teacher
            )
        except IntegrityError:
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        # If user is CustomUser, send verification email
        if not is_teacher:
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)

            # Dynamically use SITE_URL
            verification_url = f"{settings.SITE_URL}/email-verification/{urlsafe_base64_encode(str(user.id).encode())}/{token}/"
            send_email_verification.delay(user.email, verification_url)

        return user


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data["email"]
        password = data["password"]

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid credentials.")
        
        if not user.is_active:
            raise serializers.ValidationError("Account is not active.")
        
        return {
            "access": str(RefreshToken.for_user(user).access_token),
            "refresh": str(RefreshToken.for_user(user)),
        }


class TeacherLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        # Use the authenticate method to check credentials
        user = authenticate(request=self.context.get("request"), username=email, password=password)
        if user is None:
            raise serializers.ValidationError("Invalid credentials.")

        # Validate role against the authenticated user
        if role == "school_admin" and not user.is_school_admin:
            raise serializers.ValidationError("This user is not a School Admin.")
        if role == "teacher" and not user.is_teacher:
            raise serializers.ValidationError("This user is not a Teacher.")

        # Generate JWT tokens for the user
        refresh = RefreshToken.for_user(user)

        return {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "role": role,
            "message": f"{role.capitalize()} login successful",
        }


                            

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
