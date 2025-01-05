from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import models
import random

class TitleModel(models.Model):
    title = models.CharField(
        verbose_name='Başlık',
        max_length=150
    )

    class Meta:
        db_table = 'title_model'
        managed = True
        verbose_name = 'Başlık'
        verbose_name_plural = 'Öğretim Görevlileri Başlıkları'

    def __str__(self):
        return self.title

class Institution(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'Institution'
        managed = True
        verbose_name = 'Kurum'
        verbose_name_plural = 'Kurumlar'
        ordering = ['-id']

class UserProfile(models.Model):
    institution = models.ForeignKey(
        Institution, 
        on_delete=models.CASCADE,
        default='',
        null=True,
        blank=True
    )
    title = models.ForeignKey(TitleModel, on_delete=models.CASCADE, default='', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',verbose_name="Kullanıcı", error_messages={'unique':'Kullanıcı adı sistemde kayıtlı'})
    bio = models.TextField(verbose_name='Kullanıcı Biyografisi',max_length=500, blank=True, null=True)
    
    profile_picture = models.ImageField(verbose_name='Kullanıcı Profil Resmi',upload_to='profile_pictures/', blank=True, null=True, default='defaults/logo.jpg')
    is_verified = models.BooleanField(default=False, verbose_name="Kullanıcı yetkili mi ?")  
    is_active = models.BooleanField(default=False, verbose_name='Kullanıcı aktif mi ?')
    slug = models.SlugField(unique=True, blank=True) 
    contact_email = models.EmailField(verbose_name='Kullanıcıların size ulaşabileceği e-posta adresi', null=True, blank=True)


    def __str__(self):
        return self.user.username
    
    def save(self, *args, **kwargs):
        if not self.slug:
            slug_value = f'{self.user.first_name}-{self.user.last_name}-{(random.randint(1,99999))}'
            self.slug = slugify(slug_value.replace('ı','i'))
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'user_profile'
        managed = True
        verbose_name = 'profil'
        verbose_name_plural = 'Kullanıcı Profilleri'