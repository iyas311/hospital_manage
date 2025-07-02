from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from users.decorators import approved_doctor_required
from appoinments.models import Appointment
from .forms import AppointmentUpdateForm
from users.models import DoctorProfile


@login_required
@approved_doctor_required
def doctor_appointments_list(request):
    doctor = DoctorProfile.objects.get(user=request.user)
    appointments = Appointment.objects.filter(doctor=doctor).order_by('-appointment_time')
    return render(request, 'doctor/appointments_list.html', {'appointments': appointments})

from billing.forms import BillingForm  # Make sure this import is correct
from billing.models import Billing     # And this too

@login_required
@approved_doctor_required
def update_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id, doctor__user=request.user)

    # Get existing bill or create placeholder
    billing_instance = getattr(appointment, 'billing', None)
    if billing_instance is None:
        billing_instance = Billing(appointment=appointment)

    if request.method == 'POST':
        form = AppointmentUpdateForm(request.POST, instance=appointment)
        billing_form = BillingForm(request.POST, instance=billing_instance)

        if form.is_valid() and billing_form.is_valid():
            form.save()
            billing = billing_form.save(commit=False)
            billing.appointment = appointment
            billing.save()
            return redirect('doctor_dashboard')
    else:
        form = AppointmentUpdateForm(instance=appointment)
        billing_form = BillingForm(instance=billing_instance)
    
    return render(request, 'doctor/update_appointment.html', {
        'form': form,
        'billing_form': billing_form,
        'appointment': appointment
    })
