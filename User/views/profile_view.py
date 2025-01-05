from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from ..forms import UserModelForm, ProfileModelForm
from ..models import UserProfile
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.models import User
from ..forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from ..send_mail import send_email_with_template, get_client_ip

class ProfileView(LoginRequiredMixin, View):
    login_url = '/kullanici/giris-yap'
    redirect_field_name = 'next'

    def get(self, request, *args, **kwargs):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)

        user_form = UserModelForm(instance=user)
        profile_form = ProfileModelForm(instance=profile)

        return render(
            request=request,
            template_name='users/profile.html',
            context={
                'user_form':user_form,
                'profile_form':profile_form
            }
        )
    def post(self, request, *args, **kwargs):
        user = request.user
        profile, created = UserProfile.objects.get_or_create(user=user)

        user_form = UserModelForm(request.POST ,instance=user)
        profile_form = ProfileModelForm(request.POST, request.FILES, instance=profile)

        try:
            if user_form.is_valid() and profile_form.is_valid():
                with transaction.atomic():
                    email = user_form.cleaned_data.get('email')
                    title = profile_form.cleaned_data.get('instructor')

                    user_profile = request.user.profile

                    user_profile.title = title

                    user_exists = User.objects.filter(email=email).exclude(user=request.user).exists()
                    if user_exists:
                        #messages.error(request, 'E-Posta adresi ssss, tekrar deneyin')
                        return redirect(request.path)
                    else:
                        user_form.save()  
                        profile_form.save()  
                messages.success(request, 'Kullanıcı bilgileri başarıyla güncellendi.')


            else:
                for field, errors in user_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")

                for field, errors in profile_form.errors.items():
                    for error in errors:
                        messages.error(request, f"{error}")

                messages.error(request, "Girdiğiniz bilgiler doğrulanamadı. Lütfen bilgilerinizi kontrol ederek tekrar deneyiniz.")

                

        except Exception as e:
            messages.error(request, f"Hata oluştu lütfen daha sonra tekrar deneyin. {e}")


        return redirect(request.path)
       
    

class PasswordChange(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user)
        return render(
            request=request,
            template_name='users/password_change.html',
            context={'form':form}
        )
    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            send_email_with_template(
                user=request.user,
                subject='Şifre Değiştirme işlemi',
                message=(
                        'Merhaba, \n\n'
                        f'Parolanız başarıyla güncellendi. Ip Adresi: {get_client_ip(request=request)} Eğer bu işlemi siz yapmadıysanız, '
                        'lütfen hemen bizimle iletişime geçin.\n\n'
                        'Teşekkürler, \nDestek Ekibi'
                    ),
                    link=None,
                    from_mail=request.user.email,
            )
            messages.success(
                request=request,
                message='Şifreniz başarıyla değişti'
            )
            return redirect(request.path)
        else:
            messages.error(
                request=request,
                message='Lütfen geçerli bir parola girin'
            )
            return redirect(request.path)
        