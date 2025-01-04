# Randevu Sistemi

Bu proje, kullanıcıların online olarak randevu almasını ve yetkili kullanıcıların randevu yönetimi yapmasını sağlayan bir web uygulamasıdır. Uygulama, Django framework'ü ile geliştirilmiştir ve modern web teknolojileri kullanılarak tasarlanmıştır.

## Amaç

Randevu Sistemi, işletmeler veya bireyler için kolayca randevu yönetimi yapabilecekleri bir platform sunmayı amaçlar. Kullanıcılar, kayıt olduktan sonra giriş yapabilir ve uygun randevuları görebilir. Yetkili kullanıcılar ise randevuları oluşturabilir, onaylayabilir ve silebilir.


## Özellikler

- **Kullanıcı Girişi ve Kayıt**: 
  - Yeni kullanıcılar kolayca kayıt olabilir.
  - Giriş işlemleri için e-posta ve şifre doğrulaması yapılır.

- **E-posta ile Bilgilendirme**:
  - Kayıt sonrası hesap aktifleştirme e-postası gönderilir.
  - Randevu durumu değişiklikleri kullanıcıya e-posta ile bildirilir.

- **Yetkili Kullanıcı İşlemleri**:
  - Yeni randevular oluşturabilir.
  - Mevcut randevuları onaylayabilir veya silebilir.

- **Normal Kullanıcı İşlemleri**:
  - Oluşturulan randevuları görüntüleyebilir.
  - Randevu alabilir.

- **Tema Desteği**:
  - Kullanıcılar, Dark ve Light temalar arasında geçiş yapabilir.

## Kullanılan Teknolojiler

- **Frontend**:
  - HTML
  - CSS
  - SASS
  - JavaScript
  - jQuery

- **Backend**:
  - Django Framework

## Kurulum ve Çalıştırma

1. **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/ugurcl/randevu-otomasyonu.git
    cd randevu-otomasyonu
    ```

2. **Sanal Ortam Oluşturun ve Etkinleştirin:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows için: venv\Scripts\activate
    ```

3. **Bağımlılıkları Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Veritabanını Hazırlayın:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. **Geliştirme Sunucusunu Çalıştırın:**
    ```bash
    python manage.py runserver
    ```

6. **Uygulamayı Açın:**
   Tarayıcınızda [http://127.0.0.1:8000](http://127.0.0.1:8000) adresine gidin.




## Ekran Görüntüleri

![Screenshot](https://i.hizliresim.com/jisgaz1.png)

![Screen](https://i.hizliresim.com/5oi7lmz.png)

![Screen](https://i.hizliresim.com/igyviri.png)

![Screen](https://i.hizliresim.com/djvi5mo.png)
