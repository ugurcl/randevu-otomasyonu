from django.views.generic.base import TemplateView
from django.views.generic import View
from Contact.forms import ContactForm
from django.shortcuts import render, redirect
from User.models import UserProfile
from ..models import AppointmentCreation

class IndexView(View):
    template_name = 'app/index.html'
    def get(self, request, *args, **kwargs):
        profiles = UserProfile.objects.filter(is_verified=True)
        _ = AppointmentCreation.objects.filter(staff_member__in=profiles).values('staff_member')

        profiles = UserProfile.objects.filter(user__in=_)[:20]
        contact_form = ContactForm()
        return render(
            request=request,
            template_name=self.template_name,
            context={
                'form':contact_form,
                'profile':profiles
            }
        )