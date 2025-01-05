from django.urls import path
from .views import ContactViews

urlpatterns = [
    path(route='', view=ContactViews.as_view(), name='contact'),
    
]
