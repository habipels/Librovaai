# Site Ayarları Sistemi - Kullanım Kılavuzu

## 📋 Genel Bakış

Site ayarları sistemi, Librovaai platformunuzun tüm genel yapılandırmalarını veritabanında saklar ve admin panelinden yönetmenizi sağlar. Bu sayede kod değişikliği yapmadan sitenizi özelleştirebilirsiniz.

## 🎯 Özellikler

### 1. Temel Bilgiler
- **Site Adı**: Tüm sayfalarda kullanılır
- **Site Açıklaması**: Meta etiketlerde ve genel tanıtımda
- **Anahtar Kelimeler**: SEO için
- **Logo**: Navbar'da görünür (önerilen: 200x50 px)
- **Favicon**: Tarayıcı sekmesinde görünür (önerilen: 32x32 px)

### 2. İletişim Bilgileri
- **E-posta**: Footer ve iletişim sayfalarında
- **Telefon**: İletişim için
- **Adres**: Fiziksel adres bilgisi

### 3. Sosyal Medya
- Facebook, Twitter, Instagram, LinkedIn, YouTube bağlantıları
- Footer'da otomatik olarak gösterilir

### 4. Footer Ayarları
- **Footer Metni**: Telif hakkı metni
- **Footer Hakkında**: "Hakkımızda" bölümü için kısa metin

### 5. SEO Ayarları
- **Meta Başlık**: Arama motorlarında görünür
- **Meta Açıklama**: Google sonuçlarında gösterilen açıklama
- **Google Analytics ID**: Trafik izleme için (UA-XXXXXXXXX-X veya G-XXXXXXXXXX)

### 6. Sistem Ayarları
- **Bakım Modu**: Site geçici olarak kapatılır (admin hariç)
- **Bakım Modu Mesajı**: Ziyaretçilere gösterilecek mesaj
- **Varsayılan Dil**: tr (Türkçe) veya en (İngilizce)
- **Zaman Dilimi**: Örnek: Europe/Istanbul

### 7. Özellik Ayarları
- **Kullanıcı Kaydına İzin Ver**: Kapalıysa yeni kayıt yapılamaz
- **Yorumlara İzin Ver**: Kitap ve makale yorumları
- **AI İşlemeyi Etkinleştir**: Otomatik özet ve içindekiler çıkarımı

## 🚀 Kullanım

### Admin Panelinden Yönetim

1. Admin paneline giriş yapın: `/admin-panel/`
2. Sol menüden **"Site Ayarları"** seçeneğine tıklayın
3. İstediğiniz ayarları düzenleyin
4. **"Ayarları Kaydet"** butonuna tıklayın

### Django Admin'den Yönetim

1. Django admin paneline giriş yapın: `/admin/`
2. **"Site Settings"** modeline gidin
3. Tek kayıt vardır, düzenleyin ve kaydedin

## 🔧 Teknik Detaylar

### Model: `main.models.SiteSettings`

```python
# Singleton pattern kullanır
settings = SiteSettings.get_settings()
```

### Context Processor

Tüm template'lerde otomatik olarak kullanılabilir:

```django
{{ site_settings.site_name }}
{{ site_settings.logo.url }}
{{ site_settings.contact_email }}
```

### Bakım Modu

Bakım modu aktif edildiğinde:
- Normal kullanıcılar siteye erişemez
- Admin ve staff kullanıcılar erişebilir
- `/admin/`, `/login/`, `/logout/` sayfaları erişilebilir
- Özel bakım sayfası gösterilir (503 durum kodu)

Bakım modunu aktif etmek için:
1. Admin panelden "Site Ayarları"ne gidin
2. "Bakım Modu" kutucuğunu işaretleyin
3. İsteğe bağlı olarak özel mesaj yazın
4. Kaydedin

## 📝 İlk Kurulum

1. **Migration çalıştırın:**
```bash
python manage.py makemigrations
python manage.py migrate
```

2. **İlk ayarları oluşturun:**
Django shell'de:
```python
python manage.py shell

from main.models import SiteSettings
settings = SiteSettings.get_settings()
settings.site_name = "Librovaai"
settings.contact_email = "info@librovaai.com"
settings.save()
```

Veya admin panelinden `/admin/` giderek manuel olarak oluşturun.

## ⚠️ Önemli Notlar

### Singleton Pattern
- SiteSettings modelinde sadece **bir kayıt** olmalıdır
- Django admin'de yeni kayıt eklenemez
- Mevcut kayıt silinemez

### Dosya Yükleme
- Logo ve favicon için `media/settings/` klasörü kullanılır
- Desteklenen formatlar: JPG, PNG, GIF, ICO
- Önerilen boyutlar:
  - Logo: 200x50 px veya benzer oran
  - Favicon: 32x32 px veya 16x16 px

### Cache
Ayarlar her istek için sorgulanır ancak veritabanı yükü minimumdur (tek kayıt).
Yüksek trafikli siteler için cache eklenebilir:

```python
from django.core.cache import cache

def get_settings(cls):
    settings = cache.get('site_settings')
    if settings is None:
        settings, created = cls.objects.get_or_create(pk=1)
        cache.set('site_settings', settings, 3600)  # 1 saat
    return settings
```

## 🎨 Template Örnekleri

### Site Adını Gösterme
```django
<h1>{{ site_settings.site_name }}</h1>
```

### Logo Gösterme
```django
{% if site_settings.logo %}
    <img src="{{ site_settings.logo.url }}" alt="{{ site_settings.site_name }}">
{% else %}
    <h1>{{ site_settings.site_name }}</h1>
{% endif %}
```

### Sosyal Medya Linkleri
```django
{% if site_settings.facebook_url %}
    <a href="{{ site_settings.facebook_url }}" target="_blank">
        <i class="fa fa-facebook"></i>
    </a>
{% endif %}
```

### Footer
```django
<footer>
    <p>{{ site_settings.footer_text }}</p>
    <p>{{ site_settings.footer_about }}</p>
    <p>{{ site_settings.contact_email }}</p>
</footer>
```

## 🔐 Güvenlik

- Sadece admin kullanıcılar ayarlara erişebilir
- Bakım modu aktifken staff olmayan kullanıcılar siteye giremez
- Dosya yüklemeleri güvenli şekilde işlenir
- CSRF koruması aktif

## 📊 Varsayılan Değerler

Yeni kurulumda varsayılan değerler:
- Site Adı: "Librovaai"
- İletişim E-posta: "info@librovaai.com"
- Bakım Modu: Kapalı
- Kullanıcı Kaydı: Açık
- Yorumlar: Açık
- AI İşleme: Kapalı
- Varsayılan Dil: Türkçe
- Zaman Dilimi: Europe/Istanbul

## 🐛 Sorun Giderme

### "SiteSettings matching query does not exist" hatası
Çözüm:
```python
python manage.py shell
from main.models import SiteSettings
SiteSettings.objects.create()
```

### Logo görünmüyor
- `MEDIA_URL` ve `MEDIA_ROOT` ayarlarını kontrol edin
- Dosyanın `media/settings/` klasöründe olduğunu doğrulayın
- Dosya izinlerini kontrol edin

### Bakım modu çalışmıyor
- `MaintenanceModeMiddleware`'in `settings.py`'de MIDDLEWARE listesinde olduğunu doğrulayın
- Server'ı yeniden başlatın

### Context processor çalışmıyor
- `settings.py`'de TEMPLATES > OPTIONS > context_processors listesinde `'main.context_processors.site_settings'` olduğunu doğrulayın
- Template'de `{{ site_settings.site_name }}` gibi kullanım yapıyorsanız ve çalışmıyorsa, RequestContext kullandığınızdan emin olun

## 📚 İlgili Dosyalar

- **Model**: `main/models.py` - `SiteSettings`
- **Admin**: `main/admin.py` - `SiteSettingsAdmin`
- **View**: `main/admin_views.py` - `admin_site_settings()`
- **Context Processor**: `main/context_processors.py`
- **Middleware**: `main/middleware.py` - `MaintenanceModeMiddleware`
- **Template**: `main/templates/admin_panel/site_settings.html`
- **Bakım Template**: `main/templates/maintenance.html`
- **URL**: `main/book_urls.py`

## 📞 Destek

Sorunlarınız için:
1. Dokümantasyonu kontrol edin
2. Django admin log'larına bakın
3. Terminal'de hata mesajlarını inceleyin
4. Gerekirse kod içindeki yorumlara bakın
