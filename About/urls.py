from django.urls import path
from .views import IndexView

urlpatterns = [
    path(route='', view=IndexView.as_view(), name='about')
]
