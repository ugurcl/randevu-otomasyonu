from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from ..models import AppointmentCreation, AppointmentDetails
from User.send_mail import send_email_with_template
from ..mixins import VerifiedUserMixin
from ..forms import CreateAppointmentForm
from User.models import UserProfile

class UpdateCreatedAppointment(VerifiedUserMixin,View):
    template_name = "appointment/created-appointment-update.html"
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id', None)
        if id is not None:
            appointment = AppointmentCreation.objects.get(id=id)
            form = CreateAppointmentForm(initial={
                'date':appointment.date,
                'time':appointment.time,
                'appointment_is_active':appointment.appointment_is_active
            })

            return render(
                request=request,
                template_name=self.template_name,
                context={'form': form}
            )
        else:
            return redirect('create_appointment')
        
    def post(self, request, *args, **kwargs):
        form = CreateAppointmentForm(request.POST)
        id = kwargs.get('id', None)
        if form.is_valid():
            user_profile = UserProfile.objects.get(user=request.user)
            appointment = AppointmentCreation.objects.get(id=id)
        
            try:
                appointment_details = AppointmentDetails.objects.get(appointment=appointment, appointment__staff_member=user_profile)
                appointment.time = form.cleaned_data.get('time') 
                appointment.date = form.cleaned_data.get('date')
                appointment.appointment_is_active = form.cleaned_data.get('appointment_is_active')
                appointment.save()
                send_email_with_template(
                        user=appointment_details.customer.user,
                        subject="Randevunuz düzenlendi",
                        message=f'{appointment.staff_member.user.get_full_name()} Adlı öğretim görevlisinden aldığınız {appointment.date} {appointment.time} tarihli randevunuz düzenlendi. Yeni randevu {form.cleaned_data.get("date")} {form.cleaned_data.get("time")} randevunun aktiflik durumu { "Aktif" if form.cleaned_data.get("appointment_is_active") else "Dolu"} olarak düzenlendi.',
                        from_mail=appointment_details.customer.user.email,
                        link=None
                    
                    )
                messages.success(request, 'Randevunuz güncellendi.')
                       
                return redirect(request.path)
            except:
                    apointment_update = AppointmentCreation.objects.get(staff_member=user_profile, date=appointment.date, time=appointment.time)
                    apointment_update.time = form.cleaned_data.get('time') 
                    apointment_update.date = form.cleaned_data.get('date')
                    apointment_update.appointment_is_active = form.cleaned_data.get('appointment_is_active')
                    apointment_update.save()
                    messages.success(request, 'Randevunuz güncellendi.')
                    return redirect(request.path)
        else:
            return redirect(request.path)


class DeleteCreatedAppointment(VerifiedUserMixin,View):
    def get(self, request, *args, **kwargs):
        appointment_id = kwargs.get('id')
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            appointment = AppointmentCreation.objects.get(id=appointment_id, staff_member=user_profile)
            
            try:
                appointment_details = AppointmentDetails.objects.get(appointment=appointment)
                if not appointment_details.appointment.staff_member.user == request.user:
                    return redirect('create_appointment')
                
                appointment.delete()
                send_email_with_template(
                    user=appointment_details.customer.user,
                    subject=f'Randevunuz Silindi',
                    message=f'{appointment.date} {appointment.time} Tarihi için {appointment_details.appointment.staff_member.user.get_full_name()} Adlı öğretim görevlisinden Almış olduğunuz randevu silindi.',
                    from_mail=appointment_details.customer.user.email,
                    link=None
                )
                

            except:
                appointment.delete()
                send_email_with_template(
                user=appointment.staff_member.user,
                subject=f'Randevunuz Silindi',
                message=f'{appointment.date} {appointment.time} Tarihi için oluşturmuş olduğunuz randevuyu sildiniz.',
                from_mail=appointment.staff_member.user.email,
                link=None
            )

            
            return redirect('create_appointment')  
        
        except AppointmentDetails.DoesNotExist:
            
            return redirect('create_appointment')  


class DeleteAppointment(VerifiedUserMixin, View):
    def post(self, request, *args, **kwargs):
        appointment_id = kwargs.get('id')
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            try:
                appointment = AppointmentDetails.objects.get(id=appointment_id, appointment__staff_member=user_profile)
            except:
                return redirect('user_appointment_list')

            send_email_with_template(
                user=appointment.customer.user,
                subject=f'Randevunuz Silindi',
                message=f'{appointment.appointment.staff_member.user.get_full_name()} Adlı öğretim görevlisinden {appointment.appointment.date} {appointment.appointment.time} Tarihinde  aldığınız randevu silinmiştir. ',
                from_mail=appointment.customer.user.email,
                link=None
            )
            appointment.delete()
            messages.success(
                request=request,
                message='Randevu başarıyla silindi.'
            )
            return redirect('user_appointment_list')  
        
        except AppointmentDetails.DoesNotExist:
            messages.error(
                request=request,
                message='Randevu silinemedi! Tekrar deneyin.'
            )
            return redirect('user_appointment_list')  

class EditAppointmentVerifiedUser(VerifiedUserMixin, View):
    def post(self, request, *args, **kwargs):
        appointment_id = kwargs.get('id')
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            appointment = AppointmentDetails.objects.get(id=appointment_id, appointment__staff_member=user_profile )
            user = appointment.customer.user
            status = request.POST.get('status')

            if status == 'Onaylandı':
                send_email_with_template(
                    user=user,
                    subject=f'Randevunuz {status}',
                    message=f'{appointment.appointment.staff_member.user.get_full_name()} Adlı öğretim görevlisinden {appointment.appointment.date} {appointment.appointment.time} tarihi için  aldığınız randevu onaylanmıştır. ',
                    from_mail=user.email,
                    link=None
                )
            elif status == 'İptal Edildi':
                appointment_creation = appointment.appointment
        
                appointment_creation.appointment_is_active = True
                appointment_creation.save()
                send_email_with_template(
                    user=user,
                    subject=f'Randevunuz {status}',
                    message=f'{appointment.appointment.staff_member.user.get_full_name()} Adlı öğretim görevlisinden {appointment.appointment.date} {appointment.appointment.time} tarihinde aldığınız randevu iptal edilmiştir. ',
                    from_mail=user.email,
                    link=None
                )
            appointment.status = status
            appointment.save()

        except AppointmentDetails.DoesNotExist:
            
            return redirect('user_appointment_list')  

        return redirect('user_appointment_list')