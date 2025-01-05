from django.contrib import admin
from .models import AppointmentCreation, AppointmentDetails
from django.utils.html import format_html

@admin.register(AppointmentCreation)
class AppointmentCreationModelAdmin(admin.ModelAdmin):
    list_display = ('id','staff_member','status_display','formatted_date','formatted_time')


    def formatted_date(self, obj):
        return obj.date.strftime('%d.%m.%Y') 
    
    def formatted_time(self, obj):
        return obj.time.strftime('%H:%M')
   
    def status_display(self, obj):
        if obj.appointment_is_active:
            return format_html('<span style="color: #32de84;">Boş</span>')
        else:
            return format_html('<span style="color: #EF0107;">Dolu</span>')
        
        
    formatted_date.short_description = "Tarih"
    formatted_time.short_description = "Saat"
    status_display.short_description = "Durum"

@admin.register(AppointmentDetails)
class AppointmentDetailModelAdmin(admin.ModelAdmin):
    list_display = ('id','appointment','appointment_type','customer','format_notes','format_status','appointment_hour','appointment_minut')

    def format_notes(self, obj):
        return obj.notes if len(obj.notes) < 50 else obj.notes[:50] + "..."
    
    def format_status(self, obj):
        if obj.status == 'Onaylandı':
            return format_html('<span style="color: #32de84;">Aktif</span>')
        elif obj.status == 'İptal Edildi':
            return format_html('<span style="color: #EF0107;">İptal edildi</span>')
        else:
            return format_html('<span style="color: #FFD700;">Beklemede</span>')
        
    format_status.short_description = "Randevu durumu"
    format_notes.short_description = 'Randevu notu'
