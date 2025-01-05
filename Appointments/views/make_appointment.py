from ..models import AppointmentCreation,AppointmentDetails
from django.views.generic import View
from django.shortcuts import render, redirect
from User.models import UserProfile
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from ..forms import MakeAppointmentForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from User.send_mail import send_email_with_template
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.db import transaction

class GetAppointmentTimes(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        date_str = request.GET.get('date')
        slug = request.GET.get('slug')
        if date_str:
            try:
                user_profile = get_object_or_404(UserProfile, slug=slug)
                selected_date = datetime.strptime(date_str, '%d-%m-%Y').date() 
                appointments = AppointmentCreation.objects.filter(date=selected_date, appointment_is_active=True,staff_member=user_profile)
                times = appointments.values_list('time', flat=True)
                return JsonResponse({'times': list(times)})
            except ValueError:
               return JsonResponse({'error': 'Geçersiz tarih formatı'}, status=400)
        return JsonResponse({'error': 'Tarih parametresi eksik'}, status=400)

class MakeAppointmentView(LoginRequiredMixin,View):
    login_url = '/kullanici/giris-yap/' 
    redirect_field_name = None
    def get(self, request, slug, *args, **kwargs):
        form = MakeAppointmentForm()
        user_profile = get_object_or_404(UserProfile, slug=slug)
        user_appointment = AppointmentCreation.objects.filter(staff_member=user_profile,appointment_is_active=True).values('date')

        unique_dates = {item['date'] for item in user_appointment}  
        date_list = [date.strftime('%d-%m-%Y') for date in unique_dates]

        return render(
            request=request,
            template_name='appointment/book-appointment.html',
            context={'profile':user_profile,'appointment': date_list,'form':form}
        )

    def post(self, request, slug, *args, **kwargs):
    # Form verilerini al
        appointment_date = request.POST.get('appointment_date', '').strip()
        appointment_time = request.POST.get('appointment_time', '').strip()
        appointment_type = request.POST.get('appointment_type', '').strip()
        time = request.POST.get('time', '').strip()
        content = request.POST.get('content', '').strip()

   
        if not all([appointment_date, appointment_time, appointment_type, time, content]):
            messages.error(
                request=request,
                message='Tüm alanlar dolu olmak zorundadır'
            )
            return redirect(request.path)

        format_date = datetime.strptime(appointment_date, '%d-%m-%Y').date()


        user_profile = get_object_or_404(UserProfile, slug=slug)
        customer_user = get_object_or_404(UserProfile, user=request.user)

        try:
         
            with transaction.atomic():
             
                try:
                    appointment = AppointmentCreation.objects.get(
                        staff_member=user_profile,
                        date=format_date.strftime('%Y-%m-%d'),
                        time=appointment_time,
                    )
                except AppointmentCreation.DoesNotExist:
                    messages.error(
                        request=request,
                        message='Seçilen tarih ve saat için uygun bir randevu bulunamadı.'
                    )
                    return redirect(request.path)

                if not appointment.appointment_is_active:
                    messages.error(
                        request=request,
                        message='Bu randevu zaten dolu.'
                    )
                    return redirect(request.path)

                appointment.appointment_is_active = False
                appointment.save()

                AppointmentDetails.objects.create(
                    appointment=appointment,
                    appointment_type=appointment_type,
                    customer=customer_user,
                    notes=content,
                    appointment_hour=int(str(time).split(':')[0]),
                    appointment_minut=int(str(time).split(':')[1]),
                )

    
            messages.success(
                request=request,
                message='Randevu başarıyla alındı, Randevunuz onaylandığında mail üzerinden bilgilendirme yapılacaktır.'
            )

            send_email_with_template(
                user=user_profile.user,
                subject="Yeni Bir Randevu Alındı",
                message=(
                    f"Sayın {user_profile.user.get_full_name()}, "
                    f"{request.user} adlı kullanıcı sizden yeni bir randevu aldı. "
                    f"Randevu konusu: {content}"
                ),
                link=None,
                from_mail=user_profile.user.email,
            )
            return redirect(request.path)

        except IntegrityError:
            
            messages.error(
                request=request,
                message='Bu randevu alınmak için uygun değil.'
            )
            return redirect(request.path)