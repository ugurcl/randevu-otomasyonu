from django.contrib import admin
from django.urls import path, include,re_path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from Settings import views
from django.views.static import serve

handler404 = views.custom_404_view

urlpatterns = [
    path('path_0d5a8632e95117ed76def8fb18ba2176162d540d7d1/', admin.site.urls),
    path(route='', view=include('Appointments.urls')),
    path(route='hakkimizda/', view=include('About.urls')),
    path(route='kullanici/', view=include('User.urls')),
    path(route='iletisim/', view=include('Contact.urls')),
]

if not settings.DEBUG:
    
    urlpatterns += re_path(
       r'^static/(?P<path>.*)$', serve, dict(document_root=settings.STATIC_ROOT)),
    urlpatterns += re_path(
       r'^media/(?P<path>.*)$', serve, dict(document_root=settings.MEDIA_ROOT)),
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)