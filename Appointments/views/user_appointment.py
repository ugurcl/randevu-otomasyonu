from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,redirect
from ..models import AppointmentDetails,AppointmentCreation
from User.models import UserProfile
from ..forms import AppointmentStatusForm
from django.db.models import Q


class UserAppointmentsList(LoginRequiredMixin, View):
    template_name = 'appointment/user-appointment-list.html'
 

    def get(self, request, *args, **kwargs):
        try:
            _userProfile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return redirect('index')

        if _userProfile.is_verified:
            form = AppointmentStatusForm()

            appointments = AppointmentCreation.objects.filter(staff_member=_userProfile)
            appointment_details = AppointmentDetails.objects.filter(
                Q(appointment__in=appointments) | Q(customer=_userProfile)
            )

            return render(
                request=request,
                template_name='appointment/verified-user-appointment-list.html',
                context={
                    'appointment': appointment_details,
                    'form': form
                }
            )

        # Doğrulanmamış kullanıcılar için müşteri randevuları
        user_appointment = AppointmentDetails.objects.filter(customer=_userProfile)

        return render(
            request=request,
            template_name=getattr(self, 'template_name', 'default_template.html'),
            context={'appointment_list': user_appointment}
        )
