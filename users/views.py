from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.urls import reverse
from django.middleware.csrf import get_token
from django.contrib.auth.forms import AuthenticationForm
from appoinments.models import Appointment
from .forms import CustomUserCreationForm, DoctorProfileForm, PatientProfileForm, LoginForm
from .models import CustomUser, DoctorProfile, PatientProfile
from .decorators import patient_required,approved_doctor_required
from django.utils import timezone
# Helper to generate CSRF input field for inline logout form
def csrf_input(request):
    token = get_token(request)
    return f'<input type="hidden" name="csrfmiddlewaretoken" value="{token}">'


# -------------------------------
# User Registration & Login/Logout
# -------------------------------

def register(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(request, user)
            print("User type:", user.user_type)

            if user.user_type == 'doctor':
                return redirect('edit_doctor_profile', user.id)
            elif user.user_type == 'patient':
                return redirect('edit_patient_profile', user.id)
            return redirect('login')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': user_form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect based on user type
            if user.user_type == 'admin':
                return redirect('admin_dashboard')
            elif user.user_type == 'doctor':
                return redirect('doctor_dashboard')
            elif user.user_type == 'patient':
                return redirect('patient_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# -------------------------------
# Edit Profile Views
# -------------------------------

@login_required
def edit_doctor_profile(request, user_id):
    if request.user.user_type != "doctor":
        return HttpResponseForbidden()

    user = get_object_or_404(CustomUser, id=user_id)

    # Get or create DoctorProfile
    profile, _ = DoctorProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = DoctorProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')
    else:
        form = DoctorProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form, 'type': 'Doctor'})


@login_required
def edit_patient_profile(request, user_id):
    if request.user.user_type != "patient":
        return HttpResponseForbidden()

    user = get_object_or_404(CustomUser, id=user_id)
    profile, _ = PatientProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('patient_dashboard')
    else:
        form = PatientProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form, 'type': 'Patient'})


# -------------------------------
# Dashboard Views
# -------------------------------

@login_required
def admin_dashboard(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden("Admins only.")
    return render(request, 'users/admin_dashboard.html')


@login_required
@approved_doctor_required
def doctor_dashboard(request):
    doctor = DoctorProfile.objects.get(user=request.user)
    upcoming = Appointment.objects.filter(
        doctor=doctor,
        appointment_time__gte=timezone.now(),
        status="Pending"
    ).order_by('appointment_time')
    
    return render(request, 'users/doctor_dashboard.html', {
        'appointments': upcoming
    })

@login_required
@patient_required
def patient_dashboard(request):
    
    patient_profile = PatientProfile.objects.get(user=request.user)

    
    pending_appointments = Appointment.objects.filter(
        patient=patient_profile,
        status='Pending'
    ).order_by('appointment_time')

    
   
    return render(request, 'users/patient_dashboard.html', {
        'appointments': pending_appointments
    })


from django.shortcuts import redirect

def home_redirect(request):
    return redirect('login') 