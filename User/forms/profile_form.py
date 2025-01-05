from django import forms
from django.contrib.auth.models import User
from ..models import UserProfile, TitleModel
from django.core.validators import RegexValidator
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.core.validators import FileExtensionValidator


class UserModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)  
        super().__init__(*args, **kwargs)
    
    username = forms.CharField(
        widget=forms.TextInput(),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZçÇğĞıİşŞüÜöÖ\s\-]+$',
                message="Kullanıcı adınız uygun değil"
            ),
            MinLengthValidator(4,message='Kullanıcı adı minimum 4 karakter olmak zorundadır.'), 
            MaxLengthValidator(30, message='Kullanıcı adı maximum 30 karakter olmak zorundadır.'),
        ],
        error_messages={
            'required': 'Bu alan zorunludur.',
            'invalid': 'Geçersiz bir kullanıcı adı girdiniz.',
        }
        
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZçÇğĞıİşŞüÜöÖ\s\-]+$',
                message="Adınız yanlızca harf, boşluk ve tire içerebilir ve minimum 3 karakter olmak zorundadır."
            ),
            MinLengthValidator(2), 
            MaxLengthValidator(50),
        ]
    )
    
    last_name = forms.CharField(
        
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZçÇğĞıİşŞüÜöÖ\s\-]+$',
                message="Soyadınız yanlızca harf, boşluk ve tire içerebilir ve minimum 3 karakter olmak zorundadır."
            ),
            MinLengthValidator(3, message="Soyad minimum 3 karakter olmak zorundadır."), 
            MaxLengthValidator(80, message='Soyadı maximum 80 karakter olmak zorundadır.'),
        ]
    )
    

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_.+-]+@(gmail\.com|hotmail\.com|bingol\.edu\.tr)$',
                message="E-Posta formatı uygun değil tekrar deneyin"
            )
        ]
    )
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.request:
            user = self.request.user
            if User.objects.filter(username=username).distinct(id=user.id).exitst():
                raise forms.ValidationError("Bu kullanıcı adı zaten alınmış. Lütfen farklı bir kullanıcı adı deneyin.")
        return username


class ProfileModelForm(forms.ModelForm):
    title = forms.ModelChoiceField(
        queryset=TitleModel.objects.all(),
        required=False,
        label="Bölüm / Fakülte"
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(),
        validators=[
            MinLengthValidator(0, message="Biyografi minimum 1 karakter olmak zorundadır."),
            MaxLengthValidator(300, message='Biyografi maximum 300 karakter olmak zorundadır.'),
        ],
        error_messages={
            'required': 'Biyografi alanı boş bırakılamaz.',
        }
    )
    contact_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={'placeholder': 'İletişim E-posta adresiniz'}),
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_.+-]+@(gmail\.com|hotmail\.com|bingol\.edu\.tr)$',
                message="E-Posta formatı uygun değil tekrar deneyin"
            )
        ]
    )

    profile_picture = forms.ImageField(
        error_messages = {
        "invalid_image": 
             "Geçerli bir resim yükleyin. Yüklediğiniz dosya ya resim değil ya da bozuk bir resim dosyası.",
           
        
        },
        widget=forms.FileInput(
            
            attrs={
                'id': 'profile-image',
                'style': 'display:none',
                'onchange': 'changeProfileImage(event)',
                'accept': 'image/jpeg, image/png, image/jpg',
            }
        ),
         validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ]
       
    )



    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture','contact_email','title']
       
