from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

email_regex = r'^[a-zA-Z0-9_.+-]+@(gmail\.com|hotmail\.com|bingol\.edu\.tr)$'
class ContactModel(models.Model):
    class MessageStatus(models.TextChoices):
        UNREAD = 'OKUNMADI', 'Okunmadı'
        READ = 'OKUNDU', 'Okundu'

    user = models.ForeignKey(
        verbose_name='Kullanıcı',
        to=User,
        default='',
        null=True,
        blank=True,
        on_delete=models.DO_NOTHING
    )
    name = models.CharField(    
        verbose_name='Ad',
        max_length=100
    )
    last_name = models.CharField(
        verbose_name='Soyad',
        max_length=120
    )
    email = models.EmailField(
        verbose_name='Email',
         validators=[RegexValidator(regex=email_regex, message="Geçerli bir email adresi girin.")]
    )
    title = models.CharField(
        verbose_name='Başlık',
        max_length=200,
    )   
    content = models.TextField(
        verbose_name='Kullanıcı Mesajı'
    )
    status = models.CharField(
        max_length=8,
        choices=MessageStatus.choices,
        default=MessageStatus.UNREAD,
    )
    ip_address = models.GenericIPAddressField(
        verbose_name='Kullanıcı Ip Adresi',
        default='0.0.0.0',
        null=True,
        blank=True
    )   

    def __str__(self) -> str:
        return f'{self.name} {self.last_name} Adlı kişiden gelen mesaj.'
    
    class Meta:
        db_table = 'contactmodel'
        managed = True
        verbose_name = 'İletişim'
        verbose_name_plural = 'Kullanıcı İletişimleri'