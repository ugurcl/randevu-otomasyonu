from django import forms
from .models import ContactModel

class ContactForm(forms.ModelForm):
    class Meta:
       model   = ContactModel
       exclude = ['name','last_name','email','title','content']
       exclude = ['ip_address','user','status']
       widgets = {
           'name':forms.TextInput(attrs={'placeholder':'Adınız'}),
           'last_name':forms.TextInput(attrs={'placeholder':'Soyadınız'}),
           'email':forms.EmailInput(attrs={'placeholder':'E-Posta Adresiniz',},),
           'title':forms.TextInput(attrs={'placeholder':'Başlık'}),
           'content':forms.Textarea(attrs={'placeholder':'Mesajınız'}),

       }