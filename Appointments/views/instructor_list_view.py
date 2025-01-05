from django.views.generic import View
from User.models import UserProfile, Institution
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import JsonResponse
from User.models import UserProfile
from ..models import AppointmentCreation

class Search(LoginRequiredMixin, View):

   def get(self, request, *args, **kwargs):
      search = request.GET.get('search', '').strip()

      if not search:
         users = UserProfile.objects.filter(is_verified=True)


      else:
         search_parts = search.split()
         
         query = Q()

         query |= Q(user__first_name__icontains=search_parts[0]) | \
                  Q(user__last_name__icontains=search_parts[0]) | \
                  Q(bio__icontains=search_parts[0]) 

         for part in search_parts[1:]:
               query &= (
                  Q(user__first_name__icontains=part) |
                  Q(user__last_name__icontains=part) |
                  Q(bio__icontains=part)
               )

         query &= Q(is_verified=True)
         users = UserProfile.objects.filter(query)


      # Kullanıcı verilerini hazırlıyoruz
      content_data = []
      if users:
         for user in users:
            user_data = {
                  'slug': user.slug if user.slug and user.slug else '',
                  "title": user.title.title if user.title and user.title.title else '',
                  "first_name": user.user.first_name if user.user and user.user.first_name else '',
                  "last_name": user.user.last_name if user.user and user.user.last_name else '',
                  'bio': user.bio if user.bio else '',
                  'profile_picture': user.profile_picture.url if user.profile_picture else '',
                  'contact_email': user.contact_email if user.contact_email else '',
            }
            content_data.append(user_data)

      try:
         return JsonResponse({'data': content_data}, status=200)
      except Exception as e:
         return JsonResponse({'error': str(e)}, status=500)

class SearchInstitution(LoginRequiredMixin,View):
   def get(self, request, *args, **kwargs):
        value = request.GET.get('value', '').strip()

        if not value:
            data = UserProfile.objects.filter(is_verified=True)

        else:
            data = UserProfile.objects.filter(institution=value, is_verified=True)
       
        content_data = [
            {
                "title": _.title.title if _.title and _.title.title else '',
                "slug": _.slug if _.slug and _.slug else '',
                "first_name": _.user.first_name if _.user and _.user.first_name else '',
                "last_name": _.user.last_name if _.user and _.user.last_name else '',
                'bio': _.bio if _.bio else '',
                'profile_picture': _.profile_picture.url if _.profile_picture else '',
                'contact_email': _.contact_email if _.contact_email else '',
            } for _ in data
        ]

        return JsonResponse({'data': content_data})
      
      
   

class LoadMoreContentView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        offset = int(request.GET.get('offset', 0))  # Start from 0 initially
        limit = 10  # Always load 10 items
        profiles = UserProfile.objects.filter(is_verified=True)[offset:offset+limit]

        content_data = [
            {
                "title": _.title.title if _.title.title else '',
                "first_name": _.user.first_name if _.user.first_name else '',
                "last_name": _.user.last_name if _.user.last_name else '',
                'bio': _.bio if _.bio else '',
                'profile_picture': _.profile_picture.url if _.profile_picture else '',
                'contact_email': _.contact_email if _.contact_email else '',
                'slug': _.slug  # Add slug to each profile
            } for _ in profiles
        ]

        return JsonResponse({'content': content_data})
    
class InstructorListView(View):
   
   def get(self, request, *args, **kwargs):
      if not request.user.is_authenticated:
         return redirect("login")
      
      profiles = UserProfile.objects.filter(is_verified=True)[:20]
      institution_list = Institution.objects.all()
      return render(
         request=request,  
         template_name='appointment/profile-appointment.html',
         context={'users':profiles, 'institution_list':institution_list}
      )