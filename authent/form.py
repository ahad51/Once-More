from django import forms
from .models import Teacher

class TeacherCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Teacher
        fields = ('full_name', 'email', 'password', 'is_active')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("Password is required")
        return password

    def save(self, commit=True):
        teacher = super().save(commit=False)
        if commit:
            # Set the password and hash it before saving the teacher
            teacher.set_password(self.cleaned_data['password'])
            teacher.save()
        return teacher
