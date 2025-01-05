from django.contrib import admin
from .models import ContactModel

@admin.register(ContactModel)
class ContactAdminModel(admin.ModelAdmin):
    list_display = ('id','user__username','status','name','email','ip_address','last_name','title','format_content')
    list_editable = ('status',)
    list_filter = ('status',)
    actions = ['mark_as_read','mark_as_unread']

    def format_content(self, obj):
        if obj.content:
            return obj.content if len(obj.content) < 70 else obj.content[0:70] + '...'
        
    def mark_as_read(self, request, queryset):
        updated_count = queryset.update(status=ContactModel.MessageStatus.READ)
        self.message_user(request, f'{updated_count} mesaj okundu olarak işaretlendi.')
    
    def mark_as_unread(self, request, queryset):
        updated_cound = queryset.update(status=ContactModel.MessageStatus.UNREAD)
        self.message_user(
            request=request,
            message=f'{updated_cound} mesaj okunmadı olarak işaretlendi.' 
        )
    mark_as_read.short_description   = 'Seçilen mesajları okundu olarak işaretle.'
    mark_as_unread.short_description   = 'Seçilen mesajları okunmadı olarak işaretle.'

    format_content.short_description = 'Mesaj'
