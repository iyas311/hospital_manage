from django.shortcuts import render,redirect
from .models import Appointment, PatientProfile, DoctorProfile
from .forms import AppointmentForm
from django.contrib.auth.decorators import login_required
from users.decorators import patient_required
from billing.models import Billing

@login_required
@patient_required
def book_appointment(request):
    patient = PatientProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient
            appointment.status = 'Pending'  
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()

    return render(request, 'appointments/book_appointment.html', {'form': form})

@login_required
@patient_required
def medical_history(request):
    patient = PatientProfile.objects.get(user=request.user)
    completed_appointments = Appointment.objects.filter(patient=patient,status="Completed")
    return render(request, 'appointments/medical_history.html', {'history': completed_appointments})




@login_required
@patient_required
def billing(request):
    patient_profile = request.user.patientprofile
    bills = Billing.objects.filter(
        appointment__patient=patient_profile
    ).select_related('appointment', 'appointment__doctor'
    ).order_by('-appointment__appointment_time')  

    return render(request, 'appointments/billing.html', {'bills': bills})

from django.shortcuts import render, get_object_or_404, redirect
from billing.models import Billing
from django.contrib.auth.decorators import login_required
from users.decorators import patient_required

@login_required
@patient_required
def pay_bill(request, bill_id):
    bill = get_object_or_404(Billing, id=bill_id, appointment__patient=request.user.patientprofile)

    if request.method == 'POST':
        # Simulate payment
        bill.paid = True
        bill.save()
        return redirect('billing')  # Redirect back to billing page

    return render(request, 'appointments/pay_bill.html', {'bill': bill})

