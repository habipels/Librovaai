# 🚀 LIBROVAAI - HIZLI BAŞLANGIÇ REHBERİ

## 📦 Adım 1: Kurulum

### Gerekli Paketleri Yükleyin
```bash
cd "C:\Users\habip\Desktop\Librovaai"
pip install -r requirements.txt
```

## 🗄️ Adım 2: Veritabanı Kurulumu

### Migrasyonları Çalıştırın
```bash
python manage.py makemigrations users
python manage.py makemigrations main
python manage.py migrate
```

### Süper Kullanıcı Oluşturun (Admin)
```bash
python manage.py createsuperuser
```
- Username: admin
- Email: admin@librovaai.com
- Password: (güçlü bir şifre seçin)

## ▶️ Adım 3: Sunucuyu Başlatın

```bash
python manage.py runserver
```

Tarayıcıda açın: http://127.0.0.1:8000

## 🎯 Adım 4: İlk Ayarlar

### 1. Django Admin Paneline Giriş
- URL: http://127.0.0.1:8000/admin/
- Yukarıda oluşturduğunuz süper kullanıcı bilgileri ile giriş yapın

### 2. Kategoriler Oluşturun
Admin panelde:
1. "Categories" > "Add Category"
2. Örnek kategoriler:
   - Roman
   - Bilim Kurgu
   - Tarih
   - Bilim
   - Felsefe
   - Kişisel Gelişim

### 3. İlk Kullanıcıyı Admin Yapın
Admin panelde:
1. Users > İlgili kullanıcı
2. Role: "admin" seçin
3. Is staff: ✓ işaretleyin
4. Save

## 👤 Adım 5: Test Kullanıcıları Oluşturun

### Test Okuyucu
```python
python manage.py shell
```
```python
from users.models import CustomUser

# Okuyucu oluştur
reader = CustomUser.objects.create_user(
    username='okuyucu_test',
    email='okuyucu@test.com',
    password='test12345',
    role='reader',
    status='regular'
)

# Premium okuyucu oluştur
premium_reader = CustomUser.objects.create_user(
    username='premium_test',
    email='premium@test.com',
    password='test12345',
    role='reader',
    status='premium',
    is_premium=True
)

# Yazar oluştur
author = CustomUser.objects.create_user(
    username='yazar_test',
    email='yazar@test.com',
    password='test12345',
    role='author',
    title='academician',
    is_author_approved=True
)

print("Test kullanıcıları oluşturuldu!")
exit()
```

## 📚 Adım 6: Test Kitabı Yükleyin

### Yöntem 1: Web Arayüzü ile
1. http://127.0.0.1:8000/login/ - `yazar_test` ile giriş yapın (şifre: test12345)
2. "Yazar Paneli" > "Yeni Kitap Yükle"
3. Kitap bilgilerini doldurun
4. Bir PDF veya Word dosyası yükleyin
5. "Kitabı Yükle" butonuna tıklayın

### Yöntem 2: Django Shell ile
```python
python manage.py shell
```
```python
from main.models import Book, Category
from users.models import CustomUser

author = CustomUser.objects.get(username='yazar_test')
category = Category.objects.first()

book = Book.objects.create(
    title='Test Kitabı',
    subtitle='Örnek Alt Başlık',
    description='Bu bir test kitabıdır.',
    author=author,
    status='published',
    language='Türkçe'
)
book.categories.add(category)
book.save()

print(f"Kitap oluşturuldu: {book.title}")
exit()
```

## 🎭 Adım 7: Sistemin Rollerini Test Edin

### Okuyucu Testi (reader)
1. Logout yapın
2. `okuyucu_test` ile giriş yapın (şifre: test12345)
3. Kitapları görüntüleyin
4. Özetleri göremediğinizi doğrulayın (premium değil)

### Premium Okuyucu Testi (premium reader)
1. Logout yapın
2. `premium_test` ile giriş yapın (şifre: test12345)
3. Kitap detayına gidin
4. AI özetlerini görebildiğinizi doğrulayın

### Yazar Testi (author)
1. Logout yapın
2. `yazar_test` ile giriş yapın (şifre: test12345)
3. "Yazar Paneli"ne erişin
4. Kitap yükleme sayfasını test edin

### Admin Testi
1. Logout yapın
2. Süper kullanıcı ile giriş yapın
3. http://127.0.0.1:8000/admin-panel/ adresine gidin
4. Dashboard'u inceleyin
5. Kitap onaylama işlemini test edin

## 🤖 Adım 8: AI Özelliklerini Aktif Edin (Opsiyonel)

### OpenAI API ile
1. OpenAI hesabı oluşturun: https://platform.openai.com/
2. API Key alın
3. `djang_website/settings.py` dosyasını düzenleyin:
```python
USE_AI_PROCESSING = True
OPENAI_API_KEY = 'your-api-key-here'
```
4. OpenAI paketini yükleyin:
```bash
pip install openai
```

### AI Olmadan Test
AI özellikleri devre dışı olsa bile sistem çalışır. Basit özetler oluşturur.

## 📊 Adım 9: Admin Paneli ile Yönetim

### http://127.0.0.1:8000/admin-panel/

Admin panelde yapabilecekleriniz:
- ✅ Yazar onaylama
- ✅ Kitap onaylama/reddetme
- ✅ Kullanıcı yönetimi
- ✅ Premium üyelik verme
- ✅ Kategori yönetimi
- ✅ İstatistikleri görüntüleme

## 🔍 Sorun Giderme

### Migrasyon Hataları
```bash
python manage.py migrate --run-syncdb
python manage.py makemigrations
python manage.py migrate
```

### Static Dosya Sorunları
```bash
python manage.py collectstatic --noinput
```

### Port Zaten Kullanımda
```bash
# Farklı port kullanın
python manage.py runserver 8080
```

### PyPDF2 veya python-docx Hataları
```bash
pip install --upgrade PyPDF2 python-docx
```

## 📁 Önemli Klasörler

```
media/Books/           # Yüklenen kitap dosyaları
media/BookCovers/      # Kitap kapak görselleri
media/Users/           # Kullanıcı profil resimleri
main/templates/        # Template dosyaları
TEMPS/                 # Statik template dosyaları (CSS, JS)
```

## 🎯 Temel URL'ler

```
Ana Sayfa:          http://127.0.0.1:8000/
Kitaplar:           http://127.0.0.1:8000/books/
Giriş:              http://127.0.0.1:8000/login/
Kayıt:              http://127.0.0.1:8000/register/
Yazar Paneli:       http://127.0.0.1:8000/author/dashboard/
Admin Panel:        http://127.0.0.1:8000/admin-panel/
Django Admin:       http://127.0.0.1:8000/admin/
```

## 🎨 Özelleştirme

### Logo Değiştirme
`TEMPS/images/` klasörüne logo.png ekleyin

### Renk Teması
`TEMPS/style.css` dosyasını düzenleyin

### Email Ayarları
`djang_website/settings.py` içinde EMAIL_* ayarlarını yapılandırın

## 📝 Sonraki Adımlar

1. ✅ Daha fazla kategori ekleyin
2. ✅ Test kitapları yükleyin
3. ✅ Farklı rollerdeki kullanıcıları test edin
4. ✅ Premium özellikleri test edin
5. ✅ AI işlemeyi deneyin (API key ile)
6. ✅ Template'leri özelleştirin
7. ✅ Ödeme sistemi entegrasyonu planlayın

## 💡 İpuçları

- **DEBUG=True** olduğundan emin olun (geliştirme ortamı için)
- Test verileri oluşturmak için Django shell kullanın
- Her değişiklikten sonra sunucuyu yeniden başlatın (Ctrl+C, sonra tekrar runserver)
- Hataları terminal çıktısında kontrol edin
- Chrome DevTools (F12) ile frontend hatalarını görün

## 🆘 Yardım

Sorun yaşarsanız:
1. Terminal çıktısını kontrol edin
2. `PROJECT_DOCUMENTATION.md` dosyasını okuyun
3. Django loglarını inceleyin
4. Stack Overflow'da arayın
5. GitHub Issues açın

## ✅ Kontrol Listesi

- [ ] Paketler yüklendi
- [ ] Migrasyon tamamlandı
- [ ] Süper kullanıcı oluşturuldu
- [ ] Sunucu başlatıldı
- [ ] Admin panele giriş yapıldı
- [ ] Kategoriler eklendi
- [ ] Test kullanıcıları oluşturuldu
- [ ] Test kitabı yüklendi
- [ ] Rollerin tümü test edildi
- [ ] Admin panel işlevleri test edildi

---

🎉 **Tebrikler!** Librovaai artık çalışıyor!

Sorularınız için: admin@librovaai.com
