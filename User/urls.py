from django.urls import path
from .views import (
    LoginView,
    LogoutView,
    RegisterView,
    ProfileView,
    PasswordChange,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    PasswordResetDone
)
from .send_mail import activate_account


urlpatterns = [
    path(route='giris-yap/', view=LoginView.as_view(),name='login'),
    path(route='cikis-yap/', view=LogoutView.as_view(), name='logout'),
    path("kayit-ol/", RegisterView.as_view(), name="register"),
    path("activate/<uidb64>/<token>/", activate_account, name="activate"),
    path(route='profil/', view=ProfileView.as_view(), name='profile'),
    path(route='parola-degistirme/', view=PasswordChange.as_view(), name='password_change'),
    path(route='parola-sifirlama/', view=PasswordResetRequestView.as_view(), name='password_reset_request' ),
    path(route='parola-sifirlama/<uid>/<token>/', view=PasswordResetConfirmView.as_view(), name='password_reset_confirm' ),
     path(route='parola-sifirlama/basarili', view=PasswordResetDone.as_view(), name='password_reset_done' )
]
