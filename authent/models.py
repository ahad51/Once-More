from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_active = False
        user.is_staff = False  
        user.is_superuser = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    school_name = models.CharField(max_length=254, blank=True, null=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)  # Email verification required
    is_school_admin = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
class Teacher(models.Model):
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=128, default='defaultpassword')  

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
        if self.pk:
            self.save(update_fields=['password'])
        else:
            # Save the teacher object if it's a new object (no primary key)
            self.save()

    def __str__(self):
        return self.full_name