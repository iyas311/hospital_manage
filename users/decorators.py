from django.http import HttpResponseForbidden

def patient_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'patient':
            return HttpResponseForbidden("Patients only.")
        return view_func(request, *args, **kwargs)
    return wrapper


def doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.user_type != 'doctor':
            return HttpResponseForbidden("Doctors only.")
        return view_func(request, *args, **kwargs)
    return wrapper

from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.middleware.csrf import get_token
from django.urls import reverse
from users.models import DoctorProfile

def approved_doctor_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.user_type != 'doctor':
            return HttpResponseForbidden("Doctors only.")

        doctor = get_object_or_404(DoctorProfile, user=request.user)

        if not doctor.is_approved:
            csrf_token = get_token(request)
            logout_url = reverse('logout')
            return HttpResponse(f"""
                <div style="font-family:Arial; max-width:500px; margin:50px auto; padding:20px; 
                            border:1px solid #ddd; border-radius:8px; text-align:center;">
                    <h3 style="color:crimson;">Approval Pending</h3>
                    <p>Your account has not been approved by the admin yet.</p>
                    <form action="{logout_url}" method="post">
                        <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
                        <button type="submit" style="padding:10px 20px; background:#dc3545; 
                                color:white; border:none; border-radius:4px;">
                            Logout
                        </button>
                    </form>
                </div>
            """)

        return view_func(request, *args, **kwargs)
    return wrapper
