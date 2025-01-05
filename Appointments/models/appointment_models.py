from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from User.models import UserProfile
from django.core.exceptions import ValidationError
from datetime import date, time, timedelta, datetime



class AppointmentCreation(models.Model):
    
    staff_member = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='appointments_as_staff',
        verbose_name='Randevuyu veren kullanıcı',
        limit_choices_to={'is_verified': True},

    )
    appointment_is_active = models.BooleanField(default=True, verbose_name='Randevu Boş Mu ?')

    date = models.DateField(
        verbose_name='Tarih: ',
    )
    time = models.TimeField(verbose_name='Saat', max_length=5)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')

     


    class Meta:
        db_table = 'appointment'
        managed = True
        verbose_name = 'Randevular'
        verbose_name_plural = 'Oluşturulan Randevular'
        unique_together = ('staff_member', 'date', 'time')
        ordering = ['-id']

    def __str__(self) -> str:
        return f' {self.staff_member.user.get_full_name() if self.staff_member.user.get_full_name() else  self.staff_member.user.username} {self.date} {self.time}'
    


class AppointmentDetails(models.Model):
    appointment = models.OneToOneField(
        AppointmentCreation,
        on_delete=models.CASCADE,
        related_name="details",
        verbose_name='Randevu'
    )
    appointment_type = models.CharField(max_length=50, default="Genel", choices=[
        ("Genel", "Genel"),
        ("Ders", "Ders"),
        ("Danışmanlık", "Danışmanlık"),
        ("Sınav Hazırlığı", "Sınav Hazırlığı"),
        ("Proje", "Proje")
    ],
    verbose_name='Randevu Türü ')

    customer = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='appointments_as_customer',
        verbose_name='Randevuyu alan kullanıcı',
        default='',
        null=False,
        blank=False
    )
    notes = models.TextField(blank=True, null=True, verbose_name='Randevu notu')
    status = models.CharField(
        max_length=20,
        default="Beklemede",
        choices=[
            ("Beklemede", "Beklemede"),
            ("Onaylandı", "Onaylandı"),
            ("İptal Edildi", "İptal Edildi"),
        ],
        verbose_name='Randevu durumu')
    
    updated_at = models.DateTimeField(auto_now=True,verbose_name='Randevu güncellenme tarihi')
    appointment_hour = models.PositiveIntegerField(
        verbose_name='Randevu Süresi (Saat)',
        validators=[MaxValueValidator(24)],
        default=0,

    )
    appointment_minut = models.PositiveIntegerField(
        verbose_name='Randevu Süresi (Dakika)',
        validators=[MaxValueValidator(60)],
        default=0
    )

    def clean(self):
        if self.appointment.staff_member == self.customer:
            raise ValidationError("Yetkili kullanıcı kendisinden randevu alamaz.")
        
    def __str__(self):
        return f"Randevu Detayları: {self.appointment}"
    
    class Meta:
        db_table = 'appointment_details'
        managed = True
        verbose_name = 'Randevu'
        verbose_name_plural = 'Randevu Detayları'

 