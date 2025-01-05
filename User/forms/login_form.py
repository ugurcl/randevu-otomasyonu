from django.contrib.auth.models import User
from django import forms
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder':'Kullanıcı adınız'
        })
    )
    password = forms.CharField(
        required=True,
        max_length=150,
        widget=forms.PasswordInput(attrs={
            'placeholder':'Şifreniz'
        })
    )