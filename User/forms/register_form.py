from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        max_length=150,
        required=True,
        label="Kullanıcı Adı",
        widget=forms.TextInput(attrs={
            'placeholder': 'Kullanıcı adınızı girin',
            'class': 'form-control'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        label="Ad",
        widget=forms.TextInput(attrs={
            'placeholder': 'Adınızı girin',
            'class': 'form-control'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        label="Soyad",
        widget=forms.TextInput(attrs={
            'placeholder': 'Soyadınızı girin',
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        required=True,
        label="E-posta",
        widget=forms.EmailInput(attrs={
            'placeholder': 'E-posta adresinizi girin',
            'class': 'form-control'
        })
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Şifrenizi girin',
            'class': 'form-control'
        }),
        error_messages={
            'required': 'Şifre alanı zorunludur. Lütfen bir şifre girin.',
        }
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Şifrenizi tekrar girin',
            'class': 'form-control'
        }),
        error_messages={
            'required': 'Şifre alanı zorunludur. Lütfen bir şifre girin.',
        }
    )

    def clean_password1(self):
        password = self.cleaned_data.get('password1')

        if len(password) < 8:
            raise ValidationError("Şifreniz en az 8 karakter uzunluğunda olmalıdır.5")
        
        if password.isdigit():
            raise ValidationError("Şifreniz tamamen sayılardan oluşamaz, lütfen harf de ekleyin.")
        
        if password.lower() == password:
            raise ValidationError("Şifreniz en az bir büyük harf içermelidir.")
        
        return password

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise ValidationError("Şifreler uyuşmuyor, lütfen tekrar deneyin.")

        return password2
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        if first_name and len(first_name) < 2:
            raise ValidationError('Adınız minimum 2 karakter olmalıdır.')
        if last_name and len(last_name) < 3:
            raise ValidationError('Soyadınız minimum 3 karakter olmalıdır.')

     

        return cleaned_data
    
   
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        pattern = r'^[a-zA-Z0-9@.+_-]+$'  # Geçerli karakterler

        if not re.match(pattern, username):
            raise ValidationError('Kullanıcı adı yalnızca harf, rakam ve @/./+/-/_ karakterlerinden oluşabilir.')
        if User.objects.filter(username=username).exists():
            raise ValidationError('Kullanıcı adı zaten kayıtlı. Lütfen farklı bir kullanıcı adı seçin.')

        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('E-posta adresi zaten kayıtlı. Lütfen farklı bir e-posta adresi kullanın.')

        return email
