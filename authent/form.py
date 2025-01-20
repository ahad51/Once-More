from django import forms
from django.contrib.auth import get_user_model
from .models import Teacher

class TeacherCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ['full_name', 'email', 'is_active', 'password']

    def save(self, commit=True):
        # Create a new Teacher instance without saving to DB first
        teacher = super().save(commit=False)

        # Create a new user if the teacher doesn't have one
        if not teacher.user:
            user = get_user_model().objects.create_user(
                email=self.cleaned_data['email'],
                password=self.cleaned_data['password'],  # Password will be hashed automatically
                full_name=self.cleaned_data['full_name'],
                is_teacher=True,
            )
            teacher.user = user  # Link the user to the teacher

        # Save the teacher instance
        if commit:
            teacher.save()

        return teacher
