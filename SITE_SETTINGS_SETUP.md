# Site Ayarları Sistemi - Kurulum Kontrol Listesi ✅

## 📋 Dosya Kontrolü

### ✅ Model ve Admin
- [x] `main/models.py` - SiteSettings modeli eklendi
- [x] `main/admin.py` - SiteSettingsAdmin yapılandırıldı

### ✅ Views
- [x] `main/admin_views.py` - admin_site_settings() fonksiyonu eklendi

### ✅ URL Yapılandırması
- [x] `main/book_urls.py` - admin_site_settings URL'i eklendi

### ✅ Middleware ve Context Processor
- [x] `main/middleware.py` - MaintenanceModeMiddleware oluşturuldu
- [x] `main/context_processors.py` - site_settings oluşturuldu
- [x] `djang_website/settings.py` - Middleware ve context processor eklendi

### ✅ Templates
- [x] `main/templates/admin_panel/site_settings.html` - Ayarlar formu
- [x] `main/templates/maintenance.html` - Bakım modu sayfası
- [x] `main/templates/admin_panel/base.html` - Navigasyon güncellendi
- [x] `main/templates/frontend/base.html` - Dinamik ayarlar entegre edildi

### ✅ Dokümantasyon
- [x] `SITE_SETTINGS_GUIDE.md` - Kullanım kılavuzu oluşturuldu

---

## 🚀 Kurulum Adımları

### 1️⃣ Migration Oluştur ve Uygula

```bash
# Migration dosyasını oluştur
python manage.py makemigrations main

# Migration'ları uygula
python manage.py migrate
```

**Beklenen Çıktı:**
```
Migrations for 'main':
  main/migrations/000X_sitesettings.py
    - Create model SiteSettings
Running migrations:
  Applying main.000X_sitesettings... OK
```

### 2️⃣ İlk Ayarları Oluştur

**Seçenek A: Django Shell ile**
```bash
python manage.py shell
```

```python
from main.models import SiteSettings

# İlk ayarları oluştur
settings = SiteSettings.objects.create(
    site_name="Librovaai",
    site_description="Dijital kitap okuma ve paylaşım platformu",
    site_keywords="kitap, e-kitap, dijital kitap, okuma",
    contact_email="info@librovaai.com",
    meta_title="Librovaai - Dijital Kitap Platformu",
    meta_description="Binlerce dijital kitabı okuyun, yazarlarla buluşun",
    footer_text="© 2024 Librovaai. Tüm hakları saklıdır.",
    default_language="tr",
    timezone="Europe/Istanbul",
    allow_registration=True,
    allow_comments=True,
    enable_ai_processing=False,
    maintenance_mode=False
)

print("Site ayarları başarıyla oluşturuldu!")
print(f"Site Adı: {settings.site_name}")
print(f"ID: {settings.pk}")
```

**Seçenek B: Admin Panel ile**
1. Admin paneline giriş yap: `http://localhost:8000/admin/`
2. "Site settings" → "Add" butonuna tıkla (sadece ilk seferinde görünür)
3. Gerekli alanları doldur
4. Kaydet

### 3️⃣ Media Klasörünü Kontrol Et

```bash
# Media klasörünün var olduğundan emin ol
mkdir -p media/settings
```

**Windows için:**
```cmd
if not exist "media\settings" mkdir media\settings
```

### 4️⃣ Settings.py Kontrolü

`djang_website/settings.py` dosyasında şunları kontrol edin:

```python
# MIDDLEWARE listesinde
MIDDLEWARE = [
    ...
    'main.middleware.MaintenanceModeMiddleware',  # ✅ Bu satır olmalı
    ...
]

# TEMPLATES içinde
TEMPLATES = [
    {
        ...
        'OPTIONS': {
            'context_processors': [
                ...
                'main.context_processors.site_settings',  # ✅ Bu satır olmalı
            ],
        },
    },
]

# Media ayarları
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 5️⃣ Test Et

#### Test 1: Admin Panelde Ayarlara Erişim
```
1. http://localhost:8000/admin-panel/ adresine git
2. Sol menüden "Site Ayarları" tıkla
3. Form görünüyor mu? ✅
4. Ayarları değiştir ve kaydet
5. Başarılı mesajı göründü mü? ✅
```

#### Test 2: Context Processor
Ana sayfaya git ve sayfa kaynağını görüntüle (Ctrl+U):
```html
<!-- Şunları aramalısın: -->
<title>Librovaai - ...</title>  <!-- site_settings.site_name kullanılmalı -->
```

#### Test 3: Bakım Modu
```
1. Admin panelden "Bakım Modu"nu aktif et
2. Çıkış yap
3. Ana sayfaya git
4. Bakım modu sayfası görünüyor mu? ✅
5. Admin olarak giriş yap - erişim var mı? ✅
```

#### Test 4: Logo Yükleme
```
1. Admin panelden "Site Ayarları"ne git
2. Logo dosyası seç ve yükle
3. Kaydet
4. Ana sayfaya git
5. Logo görünüyor mu? ✅
```

#### Test 5: Sosyal Medya Linkleri
```
1. Footer'da sosyal medya URL'lerini doldur
2. Kaydet
3. Ana sayfanın footer'ına bak
4. Linkler görünüyor mu? ✅
```

---

## 🔍 Hata Kontrolü

### Migration Hatası: "No such table: main_sitesettings"
**Çözüm:**
```bash
python manage.py migrate main
```

### Hata: "SiteSettings matching query does not exist"
**Çözüm:**
```python
python manage.py shell
from main.models import SiteSettings
SiteSettings.objects.create()
exit()
```

### Hata: Context processor çalışmıyor
**Kontrol:**
1. `settings.py`'de context processor ekli mi?
2. Server yeniden başlatıldı mı?
```bash
# Server'ı yeniden başlat
# Ctrl+C ile durdur, sonra:
python manage.py runserver
```

### Hata: Middleware çalışmıyor
**Kontrol:**
1. `settings.py`'de MIDDLEWARE listesinde var mı?
2. Doğru sırada mı? (CommonMiddleware'den sonra olmalı)
3. Server yeniden başlatıldı mı?

### Media dosyaları görünmüyor
**Çözüm:**
`djang_website/urls.py`'ye ekle:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... mevcut url'ler
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## ✅ Kurulum Tamamlandı Kontrolü

Aşağıdaki tüm maddeleri işaretleyebiliyorsanız sistem hazır:

- [ ] Migration başarılı şekilde uygulandı
- [ ] İlk SiteSettings kaydı oluşturuldu
- [ ] Admin panelde "Site Ayarları" menüsü görünüyor
- [ ] Site ayarları formu açılıyor ve kaydedilebiliyor
- [ ] Ana sayfada site_name dinamik olarak gösteriliyor
- [ ] Logo yüklenebiliyor ve görünüyor
- [ ] Footer'da dinamik bilgiler gösteriliyor
- [ ] Bakım modu çalışıyor
- [ ] Django admin'de SiteSettings düzenlenebiliyor

---

## 📞 Sonraki Adımlar

1. **Özelleştirme**: Admin panelden site bilgilerinizi girin
2. **Logo ve Favicon**: Kendi görsellerinizi yükleyin
3. **SEO**: Meta başlık ve açıklamalarını optimize edin
4. **Sosyal Medya**: Hesap bağlantılarınızı ekleyin
5. **Test**: Tüm sayfaları kontrol edin

---

## 📚 Ek Kaynaklar

- `SITE_SETTINGS_GUIDE.md` - Detaylı kullanım kılavuzu
- `PROJECT_DOCUMENTATION.md` - Proje genel dokümantasyonu
- `GETTING_STARTED.md` - Başlangıç rehberi

---

**🎉 Sistem Hazır!** Artık sitenizi kod değişikliği olmadan yönetebilirsiniz.
