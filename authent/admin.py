from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Teacher
from .form import TeacherCreationForm  # Ensure you have this form defined
from .tasks import send_teacher_credentials_email

# Custom User Admin
class CustomUserAdmin(admin.ModelAdmin):
    model = get_user_model()
    list_display = ('id', 'full_name', 'email', 'is_active', 'is_school_admin', 'is_teacher')
    search_fields = ['full_name', 'email']
    list_filter = ['is_active', 'is_school_admin', 'is_teacher']

    def save_model(self, request, obj, form, change):
        # Only set the password for new users (not when updating)
        if not change:
            plain_password = form.cleaned_data["password"]
            obj.set_password(plain_password)  # This will hash the password

        super().save_model(request, obj, form, change)

    def has_add_permission(self, request):
        return not request.user.is_superuser and request.user.has_perm('authent.add_customuser')

    def has_change_permission(self, request, obj=None):
        return not request.user.is_superuser and request.user.has_perm('authent.change_customuser')

    def has_view_permission(self, request, obj=None):
        return not request.user.is_superuser and request.user.has_perm('authent.view_customuser')

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_superuser and request.user.has_perm('authent.delete_customuser')

class TeacherAdmin(admin.ModelAdmin):
    form = TeacherCreationForm  # Ensure this form is defined and has the correct fields
    list_display = ('id', 'full_name', 'email', 'is_active')
    search_fields = ['full_name', 'email']
    list_filter = ['is_active']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            if not obj.user:
                # Debugging the creation of the user
                print("Creating a new user for the teacher...")
                user = get_user_model().objects.create_user(
                    email=form.cleaned_data['email'],
                    full_name=form.cleaned_data['full_name'],
                    is_teacher=True,
                )
                obj.user = user  # Link the user to the teacher
                print(f"User created: {user}")

        if obj.password != form.cleaned_data["password"]:
            plain_password = form.cleaned_data["password"]
            obj.set_password(plain_password)

        obj.save()
        super().save_model(request, obj, form, change)

        # Call Celery task to send teacher credentials email
        if not change:
            send_teacher_credentials_email.delay(obj.id, form.cleaned_data['password'])

    def has_add_permission(self, request):
        return not request.user.is_superuser and request.user.has_perm('authent.add_teacher')

    def has_change_permission(self, request, obj=None):
        return not request.user.is_superuser and request.user.has_perm('authent.change_teacher')

    def has_view_permission(self, request, obj=None):
        return not request.user.is_superuser and request.user.has_perm('authent.view_teacher')

    def has_delete_permission(self, request, obj=None):
        return not request.user.is_superuser and request.user.has_perm('authent.delete_teacher')


# Registering models
admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Teacher, TeacherAdmin)
