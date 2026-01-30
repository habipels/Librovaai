# 📚 LIBRARIA - Dijital Kitap Platformu

## 🎯 Proje Özeti

Okuyucu-Yazar-Admin rollerine sahip, kitap yönetimi ve **AI destekli içerik işleme** sunan dijital kitap platformu.

---

## ✨ Temel Özellikler

### 🔐 Kullanıcı Rolleri

#### **Okuyucu (Normal/Premium)**
- ✅ Kitapları görüntüler ve okur
- ✅ **Premium üyeler**: Kitap özetlerini görebilir
- ✅ **Premium üyeler**: İçindekiler üzerinden bölümlere direkt erişim
- ❌ **Normal üyeler**: Özet görüntüleyemez

#### **Yazar**
- ✅ Kayıt olur (admin onayı gerekir)
- ✅ Ünvan belirtir (Öğrenci, Akademisyen, Araştırmacı vb.)
- ✅ Word veya PDF kitap yükler
- ✅ Admin onayından sonra kitapları yayınlanır
- ✅ Yazar panelinden kitaplarını yönetir

#### **Admin**
- ✅ Yazarları onaylar/reddeder
- ✅ Kitapları onaylar/yayına alır/reddeder
- ✅ Tüm kullanıcıları ve sistem ayarlarını yönetir
- ✅ AI işleme süreçlerini başlatır

---

## 🤖 AI Özellikleri

### Otomatik İşleme
Sistem her kitap için:
1. **Dosya Analizi**: PDF/Word dosyasını okur
2. **İçindekiler Oluşturma**: Bölümleri otomatik tespit eder
3. **Bölümlere Ayırma**: İçeriği bölümlere böler
4. **Özet Üretimi**: AI ile kısa, orta ve detaylı özetler oluşturur

### Desteklenen AI Servisleri
- **OpenAI GPT-4/GPT-3.5** (Önerilen)
- **Google Gemini** (Alternatif)
- **Anthropic Claude** (Gelecekte)

---

## 💎 Premium Sistem

| Özellik | Normal Üye | Premium Üye |
|---------|-----------|-------------|
| Kitap Okuma | ✅ | ✅ |
| Bölüm Gezinme | ✅ | ✅ |
| Kitap Özetleri | ❌ | ✅ |
| Bölüm Özetleri | ❌ | ✅ |
| Gelişmiş Özellikler | ❌ | ✅ |

---

## 📊 Veritabanı Modelleri

### 1. **CustomUser** (Kullanıcı)
```python
- user_role: reader / author / admin
- is_premium: Premium üyelik durumu
- is_author_approved: Yazar onay durumu
- author_title: Öğrenci, Akademisyen, vb.
- books_published: Yayınlanan kitap sayısı
```

### 2. **Book** (Kitap)
```python
- title, slug, author, co_authors
- description, isbn, category, tags
- cover_image, file (PDF/Word)
- status: draft / pending / approved / published / rejected
- is_processed, has_toc, has_summary
- view_count, rating_average
```

### 3. **Chapter** (Bölüm)
```python
- book (ForeignKey)
- title, order, level
- content (HTML)
- page_start, page_end
- parent (hiyerarşi için)
```

### 4. **BookSummary** (Özet)
```python
- book, chapter (opsiyonel)
- summary_type: short / medium / detailed
- content (AI tarafından üretilen)
- is_premium_only: True (varsayılan)
- generated_by: OpenAI / Gemini
```

### 5. **SiteSettings** (Site Ayarları)
```python
- Logo, favicon, banner ayarları
- İletişim bilgileri, sosyal medya
- SEO, Google Analytics
- enable_ai_processing: AI aktif/pasif
```

---

## 🚀 Kurulum

### 1. Gerekli Paketleri Yükle
```bash
pip install -r requirements.txt

# AI Özellikleri için (opsiyonel):
pip install openai              # OpenAI için
pip install google-generativeai # Gemini için
```

### 2. Veritabanı Migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Superuser Oluştur
```bash
python manage.py createsuperuser
```

### 4. Static Dosyaları Topla
```bash
python manage.py collectstatic
```

### 5. Sunucuyu Başlat
```bash
python manage.py runserver
```

---

## ⚙️ Konfigürasyon

### AI API Anahtarları
`settings.py` veya environment variables:

```python
# OpenAI
OPENAI_API_KEY = 'sk-...'

# Google Gemini
GEMINI_API_KEY = 'AIza...'

# AI İşleme
USE_AI_PROCESSING = True  # AI özelliklerini aktif et
```

---

## 📁 Proje Yapısı

```
Librovaai/
├── main/
│   ├── models.py          # Book, Chapter, BookSummary, SiteSettings
│   ├── admin.py           # Admin paneli konfigürasyonları
│   ├── views.py           # Kitap listeleme, detay, okuma viewleri
│   ├── urls.py            
│   └── services/
│       ├── document_processor.py  # PDF/Word işleme
│       └── ai_service.py          # AI özet üretimi
│
├── users/
│   ├── models.py          # CustomUser (roller, premium)
│   ├── admin.py           # Kullanıcı yönetimi, yazar onaylama
│   └── views.py           
│
├── templates/
│   ├── homebase.html      # Ana template
│   ├── includes/          # Header, footer, slider
│   └── books/             # Kitap template'leri (eklenecek)
│
├── media/
│   └── Books/             # Kitap dosyaları ve kapaklar
│
└── static/                # CSS, JS, images
```

---

## 🔄 İş Akışı

### Yazar Akışı
1. Kayıt ol → Rol: Yazar seç
2. Admin onayını bekle
3. Onaylandıktan sonra kitap yükle (PDF/Word)
4. Kitap admin onayına gider
5. Admin onayladığında yayına girer

### Kitap İşleme Akışı
1. Yazar kitap dosyasını yükler
2. Sistem dosyayı kaydeder
3. Admin "AI ile İşle" butonuna tıklar
4. Sistem:
   - Dosyadan metin çıkarır
   - İçindekiler oluşturur
   - Bölümlere ayırır
   - Her bölüm için Chapter kaydı oluşturur
   - AI ile özetler üretir (kısa/orta/detaylı)
   - BookSummary kayıtları oluşturur
5. Kitap "işlendi" olarak işaretlenir

### Okuyucu Akışı
1. Kitapları listele/ara
2. Kitap detayına git
3. **Premium ise**: Özeti göster
4. İçindekiler üzerinden bölümlere git
5. Kitabı oku

---

## 🎨 Admin Paneli Özellikleri

### Kitap Yönetimi
- ✅ Toplu onaylama/yayınlama/reddetme
- ✅ AI işleme başlatma
- ✅ Kitap durumu badge'leri (renkli)
- ✅ Inline Chapter düzenleme
- ✅ İstatistikler (görüntülenme, indirme)

### Kullanıcı Yönetimi
- ✅ Yazar onaylama
- ✅ Premium üyelik verme/kaldırma
- ✅ Rol ve ünvan yönetimi
- ✅ Kullanıcı istatistikleri

### Site Ayarları
- ✅ Logo, favicon, banner yönetimi
- ✅ İletişim ve sosyal medya bilgileri
- ✅ SEO ayarları
- ✅ AI işleme aktif/pasif

---

## 📝 Sonraki Adımlar

### Kalan Görevler
1. ✅ Modeller oluşturuldu
2. ✅ Admin paneli hazır
3. ✅ Dosya işleme servisleri hazır
4. ✅ AI servisleri hazır
5. ⏳ Views ve URL yapısı (devam ediyor)
6. ⏳ Template'ler
7. ⏳ Yazar paneli
8. ⏳ Okuyucu arayüzü
9. ⏳ Premium ödeme sistemi
10. ⏳ Arama ve filtreleme

---

## 🛠️ Kullanılan Teknolojiler

- **Backend**: Django 3.x
- **Database**: SQLite (geliştirme), PostgreSQL (production önerilen)
- **AI**: OpenAI GPT-4o-mini, Google Gemini
- **Dosya İşleme**: PyPDF2, python-docx
- **Frontend**: Bootstrap, jQuery
- **Rich Text**: TinyMCE

---

## 📧 Destek

Sorun veya önerileriniz için issue açabilirsiniz.

---

## 📄 Lisans

[Lisans bilgisi eklenecek]

---

**🎉 Projeniz hazır! Şimdi migration'ları çalıştırıp admin panelinden site ayarlarını yapabilirsiniz.**
