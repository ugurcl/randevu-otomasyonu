from django.shortcuts import render, redirect
from ..forms import CustomUserCreationForm
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.models import User
from ..send_mail import send_activation_email


class RegisterView(View):
    template_name = 'users/register.html'

    def get(self, request, *args, **kwargs):
        form = CustomUserCreationForm()
        return render(
            request=request,
            template_name=self.template_name,
            context={'form':form}
        )

    def post(self, request, *args, **kwargs):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(
                    request=request,
                    message='E-Posta sistemde Kayıtlı, Lütfen farklı bir mail adresi kullanın.'
                )
                return redirect(request.path)
            user = form.save(commit=False)

            user.save()
            send_activation_email(user, request)
            messages.success(
                request=request,
                message='Kayıt İşlemi Başarılı! Lütfen mailinize gelen aktivasyon linki ile hesabınızı aktif ediniz.'
            )
            return redirect(request.path)

        else:
          
            return render(
                request=request,
                template_name=self.template_name,
                context={'form':form}
            )
        
        