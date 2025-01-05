from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.views.generic import FormView,TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse_lazy
from ..forms import PasswordResetRequestForm, SetPasswordForm
from ..send_mail import send_email_with_template, get_client_ip
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


class PasswordResetRequestView(FormView):
    template_name = "users/reset-password.html"
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("password_reset_request")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')  
        return super().dispatch(request, *args, **kwargs)
    

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        EMAİL_CONTROL = User.objects.filter(email=email).exists()
        if not EMAİL_CONTROL:
            return redirect('index')
        try:
            user = User.objects.get(email=email)
            
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = self.request.build_absolute_uri(f'{uid}/{token}/')

            send_email_with_template(
                user=user,
                from_mail=user.email,
                link=reset_url,
                subject='Şifre Sıfırlama Talebi',
                message= f"Merhaba,\n\n Hesabınız için bir şifre sıfırlama talebi aldık. Ip adresi {get_client_ip(request=self.request)} Eğer bu talebi siz yaptıysanız, aşağıdaki bağlantıya tıklayarak şifrenizi sıfırlayabilirsiniz. Eğer bu talebi siz yapmadıysanız, bu mesajı dikkate almayabilirsiniz. Şifreniz güvende ve herhangi bir işlem yapılmamıştır. Not: Güvenliğiniz için bağlantının 24 saat içerisinde geçerliliğini yitireceğini unutmayın."

            )
            messages.success(self.request, f"Şifre sıfırlama bağlantısı {email[:2]}****@****.com adresine gönderildi.")
        except User.DoesNotExist:
            messages.error(self.request, "Bu e-posta adresine kayıtlı bir kullanıcı bulunamadı.")
        return super().form_valid(form)

class PasswordResetDone(TemplateView):
    template_name = 'users/pasword-reset-success-done.html'

  

class PasswordResetConfirmView(FormView):
    template_name = "users/new-password.html"
    form_class = SetPasswordForm
    success_url = reverse_lazy("password_reset_done")

    def dispatch(self, request, *args, **kwargs):
       
        self.uidb64 = kwargs.get('uid')
        self.token = kwargs.get('token')
        try:
            uid = urlsafe_base64_decode(self.uidb64).decode()
            self.user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError):
            self.user = None

        if self.user is None or not default_token_generator.check_token(self.user, self.token):
            messages.error(self.request, "Geçersiz veya süresi dolmuş bağlantı.")
            return self.render_to_response({'valid_token': False, 'form':self.form_class})
        messages.success(request=request, message='Şifre sıfırlama bağlantınız geçerli. Lütfen yeni şifrenizi belirleyin.')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        if self.user:
            self.user.set_password(form.cleaned_data['password'])
            self.user.save()
            messages.success(self.request, "Şifreniz başarıyla sıfırlandı. Şimdi giriş yapabilirsiniz.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['valid_token'] = self.user is not None
        return context
