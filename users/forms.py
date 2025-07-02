from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, DoctorProfile, PatientProfile

# Registration form that includes user_type selection
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','first_name','last_name','email', 'user_type', 'password1', 'password2']

# Login form with username and password
class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

# Doctor-specific profile form
class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = [
            'specialization',
            'phone',
            'qualification',
            'experience_years',
            'bio',
        ]

# Patient-specific profile form
class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['age','gender','phone','address','blood_group','emergency_contact']
