from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect
from django.views.generic import View
from ..forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from ..send_mail import send_email_with_template
from ..models import UserProfile
from ..send_mail import send_activation_email

class LoginView(View):
    template_name = 'users/login.html'
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(
            request=request,
            template_name='users/login.html',
            context={'form':form}
        )

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
       
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(
                request=request,
                username=username,
                password=password
            )

            if user is not None:
                profile = user.profile
                if not profile.is_active:
                     messages.error(request, "Hesabınız onaylanmamış. Lütfen e-posta adresinizi kontrol edin.")
                     send_activation_email(user, request)
                     return redirect('login')  
                else:
                    login(request, user)
                    return redirect(request.path)
            else:
                messages.error(request, "Kullanıcı adı veya şifre hatalı! Tekrar deneyin.")
                return redirect(request.path)
        else:
          
            return redirect(request.path)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        return super().dispatch(request, *args, **kwargs)

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request=request)
        return redirect('login')