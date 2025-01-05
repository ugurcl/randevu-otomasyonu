from django.db import models

class AboutPageModel(models.Model):
    title = models.CharField(
        verbose_name="Başlık",
        max_length=70,
        default='zx Üniversitesi',
    )
    description = models.TextField(
        verbose_name='Açıklama',
    )

    def __str__(self) -> str:
        return 'Hakkımızda sayfası düzenlendi.'
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Hakkımızda'
        verbose_name_plural = 'Hakkımızda Sayfa Ayarları'
    


class ImageGalleryModel(models.Model):
    image = models.ImageField(
        verbose_name='Resim',
        upload_to="upload/gallery/%Y/%m/%d",
    )
    
    def __str__(self) -> str:
        return 'Resim galerisi için resim eklendi.'
    
    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Resim Galerisi'
        verbose_name_plural = 'Resim Galerisi'