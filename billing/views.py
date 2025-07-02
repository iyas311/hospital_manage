from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Billing
from appoinments.models import Appointment
# Create your views here.
from .forms import BillingForm
from django.contrib.auth.decorators import login_required
from users.decorators import doctor_required, patient_required

@login_required
@doctor_required
def add_or_edit_bill(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    bill, created = Billing.objects.get_or_create(appointment=appointment)

    if request.method == 'POST':
        form = BillingForm(request.POST, instance=bill)
        if form.is_valid():
            form.save()
            return redirect('view_appointments')
    else:
        form = BillingForm(instance=bill)

    return render(request, 'doctor/billing_form.html', {'form': form, 'appointment': appointment})