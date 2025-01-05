from django import forms

class MakeAppointmentForm(forms.Form):
    APPOINTMENT_TYPE_CHOICES = [
        ("Genel", "Genel"),
        ("Ders", "Ders"),
        ("Danışmanlık", "Danışmanlık"),
        ("Sınav Hazırlığı", "Sınav Hazırlığı"),
        ("Proje", "Proje")
    ]
    
    appointment_type = forms.ChoiceField(
        choices=APPOINTMENT_TYPE_CHOICES,
        label="Randevu Türü",
        widget=forms.Select(
            attrs={'name':'appointment_type'}
        ),  
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
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={'placeholder':'Randevu konusunu giriniz'}
        )
    )
    