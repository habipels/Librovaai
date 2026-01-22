# 🎯 KURULUM ve BAŞLATMA REHBERİ

## ⚡ Hızlı Kurulum (5 Dakika)

### 1️⃣ Gerekli Paketleri Yükleyin
```bash
cd "C:\Users\habip\Desktop\Librovaai"
pip install -r requirements.txt
```

### 2️⃣ Veritabanını Hazırlayın
```bash
python manage.py makemigrations users
python manage.py makemigrations main
python manage.py migrate
```

### 3️⃣ Admin Kullanıcı Oluşturun
```bash
python manage.py createsuperuser
```
Örnek:
- Username: admin
- Email: admin@example.com
- Password: admin123 (güçlü şifre kullanın!)

### 4️⃣ Sunucuyu Başlatın
```bash
python manage.py runserver
```

### 5️⃣ Tarayıcıda Açın
```
http://127.0.0.1:8000
```

---

## ✅ İLK YAPILANDIRILMASI GEREKENlER

### Django Admin'de (http://127.0.0.1:8000/admin/)

1. **Kategoriler Ekleyin:**
   - Categories > Add Category
   - Örnekler: Roman, Bilim Kurgu, Tarih, Felsefe, vb.

2. **Admin Kullanıcınızı Düzenleyin:**
   - Users > admin > Edit
   - Role: "admin" seçin
   - Status: "moderator" veya "premium"
   - Save

### Test Kullanıcıları Oluşturun (Django Shell)

```bash
python manage.py shell
```

```python
from users.models import CustomUser

# Test Okuyucu
CustomUser.objects.create_user(
    username='okuyucu',
    email='okuyucu@test.com',
    password='test123',
    role='reader'
)

# Premium Okuyucu
CustomUser.objects.create_user(
    username='premium',
    email='premium@test.com',
    password='test123',
    role='reader',
    is_premium=True
)

# Yazar (onaylı)
CustomUser.objects.create_user(
    username='yazar',
    email='yazar@test.com',
    password='test123',
    role='author',
    title='academician',
    is_author_approved=True
)

print("Test kullanıcıları oluşturuldu!")
exit()
```

---

## 🎭 SİSTEMİ TEST ETME

### Test 1: Okuyucu Rolü
```
Giriş: okuyucu / test123
Test: Kitapları görüntüle, özetleri görememe
```

### Test 2: Premium Okuyucu
```
Giriş: premium / test123
Test: AI özetlerini görebilme, yer imi ekleme
```

### Test 3: Yazar Rolü
```
Giriş: yazar / test123
Test: Yazar paneli, kitap yükleme
```

### Test 4: Admin Rolü
```
Giriş: admin / [sizin şifreniz]
Test: Admin panel, onaylama işlemleri
```

---

## 📚 İLK KİTABI YÜKLEME

### Web Arayüzü ile:
1. "yazar" kullanıcısı ile giriş yapın
2. Yazar Paneli > Yeni Kitap Yükle
3. Bilgileri doldurun
4. PDF veya Word dosyası seçin
5. "Kitabı Yükle"

### Django Shell ile Test Kitabı:
```python
python manage.py shell
```

```python
from main.models import Book, Category
from users.models import CustomUser

author = CustomUser.objects.get(username='yazar')
cat = Category.objects.first()

book = Book.objects.create(
    title='Örnek Test Kitabı',
    description='Bu bir test kitabıdır.',
    author=author,
    status='published'
)
book.categories.add(cat)
print(f"Kitap oluşturuldu: {book.title}")
exit()
```

---

## 🤖 AI ÖZELLİKLERİNİ AKTİF ETME (Opsiyonel)

### Gerekli Paket:
```bash
pip install openai
```

### settings.py Düzenleyin:
```python
USE_AI_PROCESSING = True
OPENAI_API_KEY = 'sk-your-api-key-here'
```

### Test Et:
Kitap yüklerken "AI ile işle" seçeneğini işaretleyin.

---

## 🌐 ÖNEMLİ URL'LER

| Sayfa | URL | Kimler Erişebilir |
|-------|-----|-------------------|
| Ana Sayfa | / | Herkes |
| Kitaplar | /books/ | Herkes |
| Giriş | /login/ | Herkes |
| Kayıt | /register/ | Herkes |
| Yazar Paneli | /author/dashboard/ | Yazarlar |
| Kitap Yükle | /author/upload-book/ | Yazarlar |
| Admin Panel | /admin-panel/ | Adminler |
| Django Admin | /admin/ | Süper Kullanıcı |

---

## 🎯 ÖNEMLİ NOTLAR

### ✅ YAPILDI
- [x] Kullanıcı modelleri (reader, author, admin)
- [x] Kitap ve bölüm modelleri
- [x] AI entegrasyonu (PDF/Word işleme)
- [x] Premium sistem
- [x] Yetkilendirme decorator'ları
- [x] Frontend template'leri
- [x] Admin panel
- [x] Yazar paneli
- [x] Okuma sayfaları

### ⚠️ YAPILMASI GEREKENLER (İsteğe Bağlı)

1. **TEMPS Klasörü Entegrasyonu:**
   - TEMPS/css, js, images dosyalarını main/static/ altına kopyalayın
   - Template'lerdeki static dosya yollarını güncelleyin

2. **Ödeme Sistemi:**
   - Stripe/PayPal entegrasyonu
   - Premium üyelik ödeme akışı

3. **Email Sistemi:**
   - Yazar onayı email bildirimi
   - Kitap yayını bildirimi
   - Şifre sıfırlama

4. **Üretim Ayarları:**
   - DEBUG = False
   - SECRET_KEY değiştir
   - ALLOWED_HOSTS ayarla
   - PostgreSQL kurulumu

---

## 🔧 SORUN GİDERME

### Migrasyon Hatası:
```bash
python manage.py migrate --run-syncdb
rm db.sqlite3  # Dikkat: Veritabanını siler!
python manage.py migrate
```

### Static Dosya Sorunu:
```bash
python manage.py collectstatic --noinput
```

### Port Meşgul:
```bash
python manage.py runserver 8080
```

### Paket Hatası:
```bash
pip install --upgrade -r requirements.txt
```

---

## 📊 PROJE DURUMU

| Özellik | Durum | Not |
|---------|-------|-----|
| Kullanıcı Sistemi | ✅ Tamamlandı | 3 rol: reader, author, admin |
| Kitap Yönetimi | ✅ Tamamlandı | PDF/Word desteği |
| AI İşleme | ✅ Tamamlandı | Opsiyonel, basit algoritma dahil |
| Premium Sistem | ✅ Tamamlandı | Ödeme entegrasyonu yok |
| Admin Panel | ✅ Tamamlandı | Özel tasarım |
| Yazar Paneli | ✅ Tamamlandı | Kitap yükleme ve yönetim |
| Okuma Sistemi | ✅ Tamamlandı | Bölüm bazlı okuma |
| Template'ler | ✅ Tamamlandı | Frontend ve admin |
| API | ❌ Henüz Yok | REST API eklenebilir |
| Mobil Uygulama | ❌ Henüz Yok | İleride eklenebilir |

---

## 🚀 SONRAKI ADIMLAR

1. Sistemi test edin (yukarıdaki testleri yapın)
2. Kendi verilerinizi ekleyin (kategoriler, kitaplar)
3. Template'leri özelleştirin (logo, renkler)
4. Üretim ortamına hazırlayın (DEBUG=False, vb.)
5. Domain ve hosting ayarlayın

---

## 💡 HIZLI İPUÇLARI

- **Test Kullanıcıları:** okuyucu/test123, premium/test123, yazar/test123
- **Admin Panel:** http://127.0.0.1:8000/admin-panel/
- **Django Admin:** http://127.0.0.1:8000/admin/
- **Dokümantasyon:** PROJECT_DOCUMENTATION.md
- **Detaylı Kurulum:** GETTING_STARTED.md

---

## 🎉 TEBRİKLER!

Librovaai artık kullanıma hazır!

Her şey yolunda gittiyse:
- ✅ Sunucu çalışıyor
- ✅ Admin hesabı oluşturuldu
- ✅ Test kullanıcıları hazır
- ✅ Kategoriler eklendi
- ✅ Sistem test edildi

**Başarılar!** 🚀📚

---

**İletişim:** info@librovaai.com  
**Dokümantasyon:** PROJECT_DOCUMENTATION.md  
**GitHub:** (repo linki)
