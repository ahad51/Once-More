from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django import forms
from .models import CustomUser, Teacher

# CustomUserAdmin to handle the CustomUser model in the admin panel
class CustomUserAdmin(UserAdmin):
    list_display = ("email", "full_name", "is_staff", "is_active", "school_name")
    list_filter = ("is_staff", "is_active", "location", "school_name")
    search_fields = ("email", "full_name", "location", "school_name")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("full_name", "location", "school_name")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "full_name", "location", "school_name", "is_active", "is_staff"),
        }),
    )

    ordering = ("email",)

    def save_model(self, request, obj, form, change):
        """
        Customize save logic for staff users.
        Automatically assign permissions to staff users for managing Teacher model.
        """
        if obj.is_superuser:
            obj.is_superuser = False

        if obj.is_staff and not obj.is_superuser:
            content_type = ContentType.objects.get_for_model(Teacher)
            permissions = Permission.objects.filter(content_type=content_type, codename__in=[
                "add_teacher", "change_teacher", "view_teacher"
            ])
            obj.user_permissions.add(*permissions)

        obj.save()

    def has_delete_permission(self, request, obj=None):
        """
        Staff users cannot delete users.
        """
        if obj and obj.is_staff and not obj.is_superuser:
            return False
        return super().has_delete_permission(request, obj)

# Register CustomUser model with CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)

# TeacherCreationForm to handle teacher creation and password hashing
class TeacherCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ('full_name', 'email', 'is_active', 'password')

    def save(self, commit=True):
        # Save the form data to the teacher object without the password initially
        teacher = super().save(commit=False)
        
        if commit:
            teacher.save()  # Save the teacher object to get the primary key

        # Now set the password and save the teacher object again
        teacher.set_password(self.cleaned_data["password"])
        if commit:
            teacher.save(update_fields=['password'])
        
        return teacher


# TeacherAdmin to customize the Teacher model admin panel behavior
class TeacherAdmin(admin.ModelAdmin):
    form = TeacherCreationForm
    list_display = ('id', 'full_name', 'email', 'is_active')
    search_fields = ['full_name', 'email']
    list_filter = ['is_active']

    def has_add_permission(self, request):
        return not request.user.is_superuser and request.user.has_perm('authent.add_teacher')

    def has_change_permission(self, request, obj=None):
        return not request.user.is_superuser and request.user.has_perm('authent.change_teacher')

    def has_view_permission(self, request, obj=None):
        return not request.user.is_superuser and request.user.has_perm('authent.view_teacher')

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_superuser and request.user.has_perm('authent.delete_teacher')

# Register Teacher model with TeacherAdmin
admin.site.register(Teacher, TeacherAdmin)
