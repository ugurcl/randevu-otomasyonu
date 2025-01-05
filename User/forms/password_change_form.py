from django import forms
from django.contrib.auth.forms import PasswordChangeForm

class CustomPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Mevcut Parola")
    new_password1 = forms.CharField(widget=forms.PasswordInput, label="Yeni Parola")
    new_password2 = forms.CharField(widget=forms.PasswordInput, label="Yeni Parola (Tekrar)")
    