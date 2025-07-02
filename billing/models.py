# billing/models.py

from django.db import models
from appoinments.models import Appointment

class Billing(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='billing')
    
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    medicine_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    lab_tests = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    other_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0, blank=True)
    
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.total = sum([
            self.consultation_fee or 0,
            self.medicine_charges or 0,
            self.lab_tests or 0,
            self.other_charges or 0
        ])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Bill for {self.appointment.patient.user.get_full_name()} on {self.appointment.appointment_time.strftime('%Y-%m-%d %H:%M')}"
