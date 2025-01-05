from django.shortcuts import render
from django.views.generic.base import TemplateView
from .models import AboutPageModel, ImageGalleryModel

class IndexView(TemplateView):
    template_name = 'app/about.html'
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        if AboutPageModel.objects.count() > 0:
            context['about_title']  = AboutPageModel.objects.first().title 
            context['about_description'] = AboutPageModel.objects.first().description.split ('\n') 
        else:
            context['about_title']  = "Başlık Yok"
            context['about_description'] = ["Açıklama yok."]
        context['images'] = ImageGalleryModel.objects.all() or None
        
        return context
