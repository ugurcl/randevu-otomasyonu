from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render, redirect
from .models import UserProfile
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        try:
            ip = x_forwarded_for.split(',')[0].split()
        except ValueError:
            ip = '0.0.0.0'
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ' '.join(ip) or '0.0.0.0'

def send_email_with_template(user, subject:str, message:str,  from_mail:str, link:str):
    subject = subject
    context = {
        'user': user,
        'subject': subject,
        'message': message,
        'link':link
    }

    html_message = render_to_string(template_name='users/mail_template.html', context=context)
    

    send_mail(
        subject, 
        message,
         settings.EMAIL_HOST_USER,
         [str(from_mail)],
         html_message=html_message,
         fail_silently=False,
    )
  

def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        try:

            profile = user.profile
            profile.is_active = True
            profile.save()
            
            messages.success(
                request=request,
                message="Hesabınız başarıyla onaylandı, Lütfen giriş yapın"
            )
            return redirect("login")
        except UserProfile.DoesNotExist:
            messages.error(
                request=request,
                message="Kullanıcı profili bulunamadı! Tekrar deneyin"
            )
            return redirect(request.path)
    else:
        return render(request, "app/index.html")
    
def send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    activation_link = request.build_absolute_uri(f'/kullanici/activate/{uid}/{token}/')
    send_email_with_template(
        subject="Hesabınızı Aktif Edin",
        message='Hesabınızı aktifleştirmek için aşağıda bulunan bağlantıya tıklayın',
        user=user,
        from_mail=user.email,
        link=activation_link
    )
