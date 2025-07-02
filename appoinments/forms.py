from django import forms
from .models import Appointment   




from django import forms
from .models import Appointment
from django.forms.widgets import DateTimeInput
from django import forms
from django.utils import timezone
from .models import Appointment
from django.forms.widgets import DateTimeInput

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_time']
        widgets = {
            'appointment_time': DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'class': 'form-control',
                    'min': timezone.now().strftime('%Y-%m-%dT%H:%M')  
                }
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['appointment_time'].widget.attrs['min'] = timezone.now().strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        appointment_time = cleaned_data.get('appointment_time')

        if appointment_time and appointment_time < timezone.now():
            raise forms.ValidationError("Appointment time must be in the future.")

        if doctor and appointment_time:
            if Appointment.objects.filter(
                doctor=doctor,
                appointment_time=appointment_time,
                status='Pending'
            ).exists():
                raise forms.ValidationError("This doctor already has a pending appointment at that time.")

        return cleaned_data


