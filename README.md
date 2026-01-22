# 📚 Librovaai - Dijital Kitap Platformu

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-3.1+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

Rol bazlı yetkilendirme ve AI destekli içerik işleme sunan profesyonel bir dijital kitap platformu.

## ✨ Özellikler

### 👥 Üç Farklı Kullanıcı Rolü

- **Okuyucu (Reader):** Kitapları görüntüler, okur
- **Yazar (Author):** Kitap yükler, düzenler
- **Admin:** Tüm sistemi yönetir

### 🤖 AI Entegrasyonu

- Otomatik kitap özeti üretimi
- Bölüm bazlı özetler
- İçindekiler otomatik çıkarma
- OpenAI API desteği

### 💎 Premium Sistem

- Normal ve Premium üyelik seviyeleri
- Premium özellikler: AI özetleri, yer imleri, ilerleme takibi
- Esnek yetkilendirme sistemi

### 📖 Kitap Yönetimi

- PDF ve Word (DOC/DOCX) yükleme
- Otomatik dosya işleme
- Kategori sistemi
- Kitap derecelendirme ve yorumlar

### ⚙️ Dinamik Site Ayarları (YENİ!)

- **Veritabanı Tabanlı Yapılandırma:** Tüm site ayarları DB'de saklanır
- **Admin Panel Yönetimi:** Kod değişikliği olmadan ayarları güncelleyin
- **Otomatik Context Processor:** Tüm template'lerde kullanılabilir
- **Bakım Modu:** Site bakımı için özel sayfa
- **SEO Desteği:** Meta tags, Google Analytics entegrasyonu
- **Sosyal Medya:** Footer'da sosyal medya linkleri
- **Logo/Favicon:** Dinamik logo ve favicon yükleme
- **Özelleştirilebilir:** Footer metni, iletişim bilgileri, sistem ayarları

## 🚀 Hızlı Başlangıç

### Gereksinimler

- Python 3.8+
- pip
- virtualenv (önerilir)

### Kurulum

```bash
# Repoyu klonlayın
cd Librovaai

# Virtual environment oluşturun (önerilir)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Paketleri yükleyin
pip install -r requirements.txt

# Veritabanını oluşturun
python manage.py makemigrations
python manage.py migrate

# Süper kullanıcı oluşturun
python manage.py createsuperuser

# Sunucuyu başlatın
python manage.py runserver
```

Tarayıcıda açın: http://127.0.0.1:8000

### Detaylı Kurulum

Kapsamlı kurulum talimatları için [GETTING_STARTED.md](GETTING_STARTED.md) dosyasına bakın.

## 📖 Dokümantasyon

- [Proje Dokümantasyonu](PROJECT_DOCUMENTATION.md) - Tüm detaylar
- [Hızlı Başlangıç](GETTING_STARTED.md) - Adım adım kurulum
- [API Referansı](#) - Yakında

## 🏗️ Proje Yapısı

```
Librovaai/
├── main/                  # Ana uygulama
│   ├── models.py         # Veritabanı modelleri
│   ├── book_views.py     # Frontend görünümler
│   ├── admin_views.py    # Admin panel görünümler
│   ├── ai_processor.py   # AI ve dosya işleme
│   └── templates/        # HTML şablonları
├── users/                # Kullanıcı yönetimi
├── djang_website/        # Django ayarları
├── media/                # Yüklenen dosyalar
└── TEMPS/                # Statik dosyalar
```

## 🎯 Kullanım Senaryoları

### Yazar Olarak Kitap Yükleme

1. Kayıt olun ve "Yazar Ol" butonuna tıklayın
2. Admin onayını bekleyin
3. Onaylandıktan sonra "Kitap Yükle" sayfasına gidin
4. Kitap bilgilerini ve dosyasını yükleyin
5. AI işleme seçeneğini aktif edin (opsiyonel)
6. Admin onayına gönderin

### Okuyucu Olarak Kitap Okuma

1. Kayıt olun veya giriş yapın
2. Kitaplar sayfasından istediğiniz kitabı seçin
3. "Kitabı Oku" butonuna tıklayın
4. İçindekiler üzerinden istediğiniz bölüme gidin
5. Premium üye olarak AI özetlerine erişin

### Admin Olarak Yönetim

1. Admin hesabıyla giriş yapın
2. Admin Panel'e gidin (/admin-panel/)
3. Bekleyen yazarları onaylayın
4. Bekleyen kitapları inceleyin ve onaylayın
5. Kullanıcılara premium üyelik verin
6. **Site Ayarlarını Yapılandırın** (YENİ!)
   - Site adı, logo ve favicon yükleyin
   - İletişim bilgilerini güncelleyin
   - Sosyal medya hesaplarını ekleyin
   - SEO ayarlarını optimize edin
   - Bakım modunu etkinleştirin

## ⚙️ Site Ayarları Sistemi

### Admin Panelden Yönetim

Admin panel'den dinamik olarak aşağıdaki ayarları yönetebilirsiniz:

- **Temel Bilgiler**: Site adı, açıklama, logo, favicon
- **İletişim**: E-posta, telefon, adres
- **Sosyal Medya**: Facebook, Twitter, Instagram, LinkedIn, YouTube
- **Footer**: Telif hakkı metni, hakkında bilgisi
- **SEO**: Meta başlık, açıklama, Google Analytics
- **Sistem**: Bakım modu, varsayılan dil, zaman dilimi
- **Özellikler**: Kayıt izni, yorum izni, AI işleme

### Kullanım

Site ayarlarına erişim:
1. Admin Panel → Site Ayarları menüsüne tıklayın
2. Veya Django Admin → Site Settings bölümüne gidin

**Detaylı kullanım için:** [SITE_SETTINGS_GUIDE.md](SITE_SETTINGS_GUIDE.md)  
**Kurulum için:** [SITE_SETTINGS_SETUP.md](SITE_SETTINGS_SETUP.md)

## 🔧 Yapılandırma

### settings.py

```python
# AI İşleme
USE_AI_PROCESSING = True          # AI özelliklerini aktif et
OPENAI_API_KEY = 'your-api-key'   # OpenAI API anahtarı

# Dosya Boyutu
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB

# Middleware (Site ayarları için gerekli)
MIDDLEWARE = [
    ...
    'main.middleware.MaintenanceModeMiddleware',  # Bakım modu
]

# Context Processors (Site ayarları için gerekli)
TEMPLATES = [{
    'OPTIONS': {
        'context_processors': [
            ...
            'main.context_processors.site_settings',  # Site ayarları
        ],
    },
}]
```

### AI Kullanımı (Opsiyonel)

OpenAI API kullanmak için:

```bash
pip install openai
```

`settings.py` dosyasında:
```python
USE_AI_PROCESSING = True
OPENAI_API_KEY = 'sk-...'  # API anahtarınız
```

## 🛠️ Teknolojiler

- **Backend:** Django 3.1+
- **Database:** SQLite (geliştirme), PostgreSQL (üretim önerilir)
- **Frontend:** Bootstrap 3, jQuery
- **File Processing:** PyPDF2, python-docx
- **AI:** OpenAI API (opsiyonel)

## 📦 Gerekli Paketler

```
Django
Pillow
PyPDF2
python-docx
django-tinymce
django-crispy-forms
django-recaptcha
fontawesomefree
```

Tam liste için [requirements.txt](requirements.txt) dosyasına bakın.

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Pull Request açın

## 📝 To-Do Listesi

- [x] ~~Dinamik site ayarları sistemi~~
- [x] ~~Bakım modu özelliği~~
- [x] ~~SEO meta tags yönetimi~~
- [ ] Ödeme sistemi entegrasyonu
- [ ] Email bildirimleri
- [ ] REST API
- [ ] Mobil uygulama
- [ ] Kitap indirme özelliği
- [ ] Gelişmiş arama (Elasticsearch)
- [ ] Çoklu dil desteği (i18n)

## 🐛 Bilinen Sorunlar

- TEMPS klasöründeki statik dosyalar manuel olarak ayarlanmalı
- AI işleme büyük dosyalarda yavaş olabilir
- Premium ödeme sistemi henüz entegre edilmemiş

## 📄 Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 📧 İletişim

- Email: info@librovaai.com
- Website: https://librovaai.com
- GitHub: https://github.com/librovaai/platform

## 🙏 Teşekkürler

- Django Framework
- Bootstrap
- OpenAI
- Tüm açık kaynak katkıda bulunanlar

## 📸 Ekran Görüntüleri

### Ana Sayfa
![Ana Sayfa](screenshots/home.png)

### Kitap Detay
![Kitap Detay](screenshots/book-detail.png)

### Admin Panel
![Admin Panel](screenshots/admin-panel.png)

---

⭐ Bu projeyi beğendiyseniz yıldız vermeyi unutmayın!

**Geliştirici:** Librovaai Team  
**Versiyon:** 1.0.0  
**Son Güncelleme:** 2026
