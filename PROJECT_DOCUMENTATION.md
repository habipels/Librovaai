# 📚 LIBROVAAI - DİJİTAL KİTAP PLATFORMU

## 🎯 Proje Özeti

Librovaai, rol bazlı yetkilendirme (Okuyucu, Yazar, Admin) ve AI destekli içerik işleme sunan profesyonel bir dijital kitap platformudur.

## ⚡ Özellikler

### 🔐 Kullanıcı Rolleri

#### 1. Okuyucu (Öğrenci)
- ✅ Kitapları görüntüleme
- ✅ İçindekiler üzerinden gezinme
- ⭐ **Premium özellikler:**
  - AI tarafından üretilmiş kitap özetlerini okuma
  - Gelişmiş okuma özellikleri
  - Yer imleri ekleme
  - Okuma ilerlemesi takibi

#### 2. Yazar
- ✅ Kayıt olma ve admin onayı bekleme
- ✅ Ünvan seçimi (Öğrenci, Akademisyen, Araştırmacı, vb.)
- ✅ Word veya PDF kitap yükleme
- ✅ Kitap düzenleme ve yönetimi
- ✅ Yazar paneli ile istatistikler
- ✅ Otomatik kitap işleme (AI ile)

#### 3. Admin
- ✅ Yazar onaylama/reddetme
- ✅ Kitap onaylama/yayına alma
- ✅ Kullanıcı yönetimi
- ✅ Kategori yönetimi
- ✅ Premium üyelik yönetimi
- ✅ Sistem istatistikleri

### 📚 Kitap & İçerik Sistemi

- **Dosya Yükleme:** PDF ve Word (DOC/DOCX) desteği
- **Otomatik İşleme:**
  - Dosya analizi
  - İçindekiler (Table of Contents) oluşturma
  - Bölümlere ayırma
  - Veritabanına kaydetme

### 🤖 Yapay Zekâ Özellikleri

- **Otomatik Özet Üretimi:**
  - Kitap özeti
  - Bölüm özetleri
  - OpenAI API entegrasyonu (opsiyonel)
  
- **AI olmadan da çalışır:** Basit özet algoritması

### 💎 Premium Sistem

- Normal kullanıcılar kitapları okuyabilir
- Premium üyeler:
  - AI özetlerine erişir
  - Gelişmiş okuma özelliklerini kullanır
  - Yer imi ekleyebilir

## 🗂️ Proje Yapısı

```
Librovaai/
├── main/                          # Ana uygulama
│   ├── models.py                  # Book, Chapter, Category modelleri
│   ├── book_views.py              # Frontend view'leri
│   ├── admin_views.py             # Admin panel view'leri
│   ├── book_urls.py               # URL yapılandırması
│   ├── decorators.py              # Yetkilendirme decorator'ları
│   ├── ai_processor.py            # AI ve dosya işleme
│   ├── admin.py                   # Django admin yapılandırması
│   ├── templates/
│   │   ├── frontend/              # Okuyucu & yazar template'leri
│   │   │   ├── base.html
│   │   │   ├── books/
│   │   │   │   ├── books_list.html
│   │   │   │   ├── book_detail.html
│   │   │   │   ├── chapter_read.html
│   │   │   │   └── ...
│   │   │   └── author/
│   │   │       ├── dashboard.html
│   │   │       ├── upload_book.html
│   │   │       └── ...
│   │   └── admin_panel/           # Admin panel template'leri
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       └── ...
│   └── static/
│       └── ...
│
├── users/                         # Kullanıcı yönetimi
│   ├── models.py                  # CustomUser modeli (roller, premium)
│   ├── admin.py
│   └── ...
│
├── djang_website/                 # Proje ayarları
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── TEMPS/                         # Statik template dosyaları
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                         # Yüklenen dosyalar
│   ├── Books/                     # Kitap dosyaları
│   ├── BookCovers/                # Kapak görselleri
│   └── Users/                     # Kullanıcı profil resimleri
│
├── requirements.txt
├── manage.py
└── README.md
```

## 🛠️ Kurulum

### 1. Gerekli Paketleri Yükleyin

```bash
pip install -r requirements.txt
```

**Gerekli Paketler:**
- Django
- Pillow (görsel işleme)
- PyPDF2 (PDF okuma)
- python-docx (Word okuma)
- django-tinymce
- django-crispy-forms
- django-recaptcha

**Opsiyonel (AI için):**
- openai (OpenAI API için)

### 2. Veritabanı Migrasyonları

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Süper Kullanıcı Oluşturun

```bash
python manage.py createsuperuser
```

### 4. Statik Dosyaları Toplayın

```bash
python manage.py collectstatic
```

### 5. Sunucuyu Başlatın

```bash
python manage.py runserver
```

## ⚙️ Yapılandırma

### settings.py Ayarları

```python
# AI İşleme (Opsiyonel)
USE_AI_PROCESSING = False          # True yaparak aktif edin
OPENAI_API_KEY = 'your-api-key'    # OpenAI API key

# Dosya Yükleme
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB

# Medya Dosyaları
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

## 📋 Veritabanı Modelleri

### CustomUser (users/models.py)
```python
- username, email, password (Django varsayılan)
- role: reader/author/admin
- status: regular/premium/moderator
- title: Öğrenci/Akademisyen/vb. (yazar için)
- is_author_approved: Yazar onay durumu
- is_premium: Premium üyelik
- premium_start_date, premium_end_date
```

### Book (main/models.py)
```python
- title, slug, subtitle, description
- author (ForeignKey -> CustomUser)
- categories (ManyToMany -> Category)
- file (FileField - PDF/Word)
- cover_image
- status: draft/pending/approved/published/rejected
- is_processed: Dosya işlendi mi?
- ai_summary: AI özeti
- has_toc: İçindekiler var mı?
- view_count, download_count
- publisher, isbn, publication_year, page_count, language
```

### Chapter (main/models.py)
```python
- book (ForeignKey -> Book)
- title, slug, content
- chapter_number, level, order
- parent (ForeignKey -> self, nullable)
- page_start, page_end
- ai_summary
```

### Category
```python
- name, slug, description
```

### BookRating
```python
- book, user, rating (1-5), review
```

### ReadingProgress
```python
- user, book, chapter, progress_percentage
```

### Bookmark
```python
- user, book, chapter, note
```

## 🔗 URL Yapısı

### Frontend (Okuyucu & Yazar)
```
/                           # Ana sayfa
/books/                     # Kitap listesi
/book/<slug>/               # Kitap detay
/book/<slug>/read/          # Kitap okuma
/categories/                # Kategori listesi
/my-library/                # Kullanıcı kütüphanesi
/premium/                   # Premium üyelik
/author/dashboard/          # Yazar paneli
/author/upload-book/        # Kitap yükleme
/become-author/             # Yazar başvurusu
```

### Admin Panel
```
/admin-panel/               # Dashboard
/admin-panel/books/         # Kitap yönetimi
/admin-panel/authors/       # Yazar onayları
/admin-panel/users/         # Kullanıcı yönetimi
/admin-panel/categories/    # Kategori yönetimi
/admin-panel/premium/       # Premium yönetimi
/admin-panel/statistics/    # İstatistikler
```

## 🎨 Decorator'lar

```python
@author_required           # Onaylı yazar gerekli
@admin_required           # Admin gerekli
@premium_required         # Premium üye gerekli
@book_owner_or_admin      # Kitap sahibi veya admin
@check_book_access        # Kitaba erişim kontrolü
```

## 🤖 AI İşleme Süreci

### 1. Dosya Yükleme
Yazar kitap yükler (PDF/Word)

### 2. Otomatik İşleme
```python
from main.ai_processor import process_book_file

result = process_book_file(
    book_instance=book,
    use_ai=True,
    api_key='your-openai-key'
)
```

### 3. İşlem Adımları
1. **Metin Çıkarma:** PDF/Word'den metin
2. **İçindekiler Analizi:** Başlıkları bulma
3. **Bölümlere Ayırma:** Chapter modellerine kaydetme
4. **Özet Üretimi:** AI ile veya basit algoritma

## 📊 Kullanım Senaryoları

### Senaryo 1: Yeni Yazar Kaydı
1. Kullanıcı kayıt olur
2. "Yazar Ol" sayfasına gider
3. Ünvan seçer, bio yazar
4. Admin onayını bekler
5. Admin onayladığında kitap yükleyebilir

### Senaryo 2: Kitap Yükleme
1. Yazar, "Kitap Yükle" sayfasına gider
2. Kitap bilgilerini doldurur
3. PDF/Word dosyası seçer
4. "AI ile işle" seçeneğini işaretler (opsiyonel)
5. "Admin Onayına Gönder" veya "Taslak" seçer
6. Sistem dosyayı işler ve bölümlere ayırır
7. Admin kitabı onaylar
8. Kitap yayına alınır

### Senaryo 3: Okuyucu Deneyimi
1. Okuyucu kitap listesine göz atar
2. Kitap detayına gider
3. İçindekiler üzerinden bölüm seçer
4. Okuma ilerlemesi otomatik kaydedilir
5. Premium ise özeti okuyabilir

## 🔒 Güvenlik

- Rol bazlı erişim kontrolü
- Decorator'larla view koruması
- Dosya yükleme limitleri (50MB)
- CSRF koruması
- Login gerektiren sayfalar

## 🚀 Üretim (Production) İçin Notlar

1. **DEBUG = False** yapın
2. **SECRET_KEY** değiştirin
3. **ALLOWED_HOSTS** ayarlayın
4. Statik dosyaları bir CDN'e taşıyın
5. Veritabanı olarak PostgreSQL kullanın
6. Redis ile caching ekleyin
7. Celery ile arka plan işlemleri
8. Nginx + Gunicorn kullanın

## 📝 Yapılabilecek Geliştirmeler

- [ ] Ödeme sistemi entegrasyonu (Premium için)
- [ ] Kitap indirme özelliği
- [ ] E-posta bildirimleri
- [ ] Sosyal medya paylaşımı
- [ ] Kitap yorumları ve tartışma forumu
- [ ] Kitap koleksiyonları
- [ ] Okuma çevrimi (offline okuma)
- [ ] Gelişmiş arama (Elasticsearch)
- [ ] API (REST/GraphQL)
- [ ] Mobil uygulama

## 🐛 Sorun Giderme

### Migrasyon Hataları
```bash
python manage.py migrate --run-syncdb
```

### Statik Dosya Sorunları
```bash
python manage.py collectstatic --clear
```

### AI İşleme Çalışmıyor
1. PyPDF2 ve python-docx yüklü mü kontrol edin
2. USE_AI_PROCESSING=False ise basit özet kullanır
3. OpenAI API key doğru mu kontrol edin

## 📞 Destek

Herhangi bir sorun için:
1. GitHub Issues açın
2. Dokümantasyonu okuyun
3. Stack Overflow'da arayın

## 📜 Lisans

Bu proje eğitim amaçlıdır.

---

**Geliştirici Notları:**

- Tüm modeller Türkçe field adları ile oluşturulmuştur
- Template'ler Bootstrap 3 ile tasarlanmıştır
- TEMPS klasöründeki statik dosyalar mevcut yapıya entegre edilebilir
- AI işleme opsiyoneldir, sistem AI olmadan da çalışır
- Premium sistem temeldir, ödeme entegrasyonu eklenmemiştir

**Önemli:** Üretim ortamına geçmeden önce güvenlik ayarlarını mutlaka gözden geçirin!
