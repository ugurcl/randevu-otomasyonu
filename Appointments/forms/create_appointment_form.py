from django.core.exceptions import ValidationError
from ..models import AppointmentCreation
from datetime import date
from django import forms

class CreateAppointmentForm(forms.Form):
    date = forms.DateField(
        widget= forms.DateInput(
            attrs={
                'type':'date'
            },
             format='%Y-%m-%d'
        ),
        input_formats=['%Y-%m-%d'],
        required=True
    )

    time = forms.TimeField(
        widget= forms.TimeInput(
            attrs={
                'type':'time'
            },
             format='%H:%M'
        ),
        input_formats=['%H:%M'],
        required=True
    )
   
    appointment_is_active = forms.BooleanField(required=False)


    def clean_date(self):
        selected_date = self.cleaned_data['date']
        if selected_date < date.today():
            raise ValidationError("Geçmiş bir tarih seçemezsiniz.")
        return selected_date