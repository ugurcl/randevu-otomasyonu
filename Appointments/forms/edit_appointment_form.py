from django import forms
from ..models import AppointmentDetails

class AppointmentStatusForm(forms.ModelForm):
    class Meta:
        model = AppointmentDetails
        fields = ['status']
        widgets = {
            'status': forms.Select(
                
                choices=AppointmentDetails._meta.get_field('status').choices
                )
        }