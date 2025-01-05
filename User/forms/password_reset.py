from django import forms
from django.contrib.auth.models import User
import re

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder':'E-Posta adresinizi giriniz',
            }
        )
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError(message='Bu E-Posta adresine kayıtlı bir kullanıcı bulunamadı')
        return email
    
class SetPasswordForm(forms.Form):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Yeni şifrenizi girin',

        }),
        min_length=8
    )
    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Yeni şifrenizi tekrar girin',
        }),
        min_length=8
    )

    def clean_password(self):
        password = self.cleaned_data.get('password')
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'
        if not re.match(pattern, password):
            raise forms.ValidationError(
                "Şifre en az 8 karakter, bir büyük harf, bir küçük harf ve bir rakam içermelidir."
            )
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Şifreler eşleşmiyor.")