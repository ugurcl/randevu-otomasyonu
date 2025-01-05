from django.contrib import admin
from .models import AboutPageModel,ImageGalleryModel
from django.utils.html import mark_safe

@admin.register(ImageGalleryModel)
class ImageGalleryModelAdmin(admin.ModelAdmin):
    list_display = ('id','image_format')

    def image_format(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="200" height="200" style="object-fit:cover; object-position:center;">')
    image_format.short_description = 'Resim'

@admin.register(AboutPageModel)
class AboutPageAdminModel(admin.ModelAdmin):
    list_display = ('id','title_format','description_format')

    def title_format(self, obj):
        return obj.title if len(obj.title) < 20 else obj.title[0:30]
    
    def description_format(self, obj):
        return obj.description if len(obj.description) < 190 else obj.description[0:190] + '...'


    title_format.short_description = 'Başlık'
    description_format.short_description = 'Açıklama'
