from django.db import models
from users.models import PatientProfile,DoctorProfile




class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    )

    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    appointment_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    diagnosis = models.TextField(blank=True, null=True)
    prescription = models.TextField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_time', 'status'],
                name='unique_pending_doctor_appointment',
                condition=models.Q(status='Pending')  # Only enforce uniqueness for Pending
            )
        ]
    def __str__(self):
        return f"Appointment with Dr. {self.doctor.user.get_full_name()} by {self.patient.user.get_full_name()} on {self.appointment_time.strftime('%Y-%m-%d %H:%M')}"


