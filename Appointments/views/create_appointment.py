from django.views.generic import View
from ..mixins import VerifiedUserMixin
from ..forms import CreateAppointmentForm
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import AppointmentCreation
from User.models import UserProfile
from datetime import datetime
from django.http import JsonResponse
    

class CreateAppointmentView(VerifiedUserMixin,View):
    template_name = 'appointment/create-appointment.html'
    
    def get(self, request, *args, **kwargs):
        form = CreateAppointmentForm()
        _profile = UserProfile.objects.get(user=request.user)
        _appointmentList = AppointmentCreation.objects.filter(staff_member=_profile).order_by('-id')
       
        return render(
            request=request,
            template_name=self.template_name,
            context={'form':form,'appointments':_appointmentList}
        )

    def post(self, request, *args, **kwargs):
        form = CreateAppointmentForm(request.POST)
      
        if form.is_valid():
            date = form.cleaned_data.get('date')
            time = form.cleaned_data.get('time')
            is_active = form.cleaned_data.get('appointment_is_active')
            user_profile = UserProfile.objects.get(user=request.user)
            _control = AppointmentCreation.objects.filter(
                staff_member=user_profile,
                date=date,
                time=time
            )
            if _control.exists():
                messages.error(
                    request=request,
                    message='Aynı tarih için oluşturulan randevunuz var, lütfen başka tarih seçiniz.'
                )
                return redirect(request.path)
            AppointmentCreation.objects.create(
                staff_member=user_profile,  
                date=date,
                time=time,
                appointment_is_active=is_active
            )
            messages.success(
                request=request,
                message='Randevu başarıyla oluşturuldu'
            )
            return redirect(request.path)
        else:
            print(form.errors)
            messages.error(
                request=request,
                message='Randevu oluşturulamadı, tekrar deneyin'
            )
            return redirect(request.path)