# billing/forms.py

from django import forms
from .models import Billing

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['consultation_fee', 'medicine_charges', 'lab_tests', 'other_charges']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  # This makes all billing fields optional
