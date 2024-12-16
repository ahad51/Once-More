from rest_framework import serializers
from .models import CustomUser

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    full_name = serializers.CharField(required=True)
    location = serializers.CharField(required=True)
    school_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password", "full_name", "location", "school_name"]

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data["full_name"],
            location=validated_data["location"],
            school_name=validated_data["school_name"],
        )
        return user
