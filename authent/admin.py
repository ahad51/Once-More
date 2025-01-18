from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Teacher
from .form import TeacherCreationForm  # Make sure you have this form defined
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
        # If the object is new, save it first to assign a primary key
        if not obj.pk:
            obj.save()

        # Set password if it's not being changed (only for new users)
        if obj.password != form.cleaned_data["password"]:
            plain_password = form.cleaned_data["password"]
            obj.set_password(plain_password)  # This will hash the password
            obj.save(update_fields=["password"])

        # Call Celery task to send teacher credentials email
        if not change:
            send_teacher_credentials_email.delay(obj.id, form.cleaned_data['password'])  # Using Celery's delay function to send the email asynchronously

        super().save_model(request, obj, form, change)

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
