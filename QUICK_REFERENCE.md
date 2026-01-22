# 🚀 Librovaai - Hızlı Referans Kılavuzu

## 📦 Temel Komutlar

### Geliştirme Sunucusu
```bash
# Sunucuyu başlat
python manage.py runserver

# Belirli port'ta başlat
python manage.py runserver 8080
```

### Database İşlemleri
```bash
# Migration oluştur
python manage.py makemigrations

# Migration uygula
python manage.py migrate

# Migration'ları geri al
python manage.py migrate main zero

# Database shell
python manage.py dbshell
```

### Django Shell
```bash
# Python shell
python manage.py shell

# IPython shell (kurulu ise)
python manage.py shell -i ipython
```

### Kullanıcı Yönetimi
```bash
# Superuser oluştur
python manage.py createsuperuser

# Kullanıcı değiştir
python manage.py changepassword username
```

### Test ve Lint
```bash
# Testleri çalıştır
python manage.py test

# Belirli app'i test et
python manage.py test main

# Coverage ile
coverage run --source='.' manage.py test
coverage report
```

---

## 🗂️ Önemli URL'ler

### Frontend
```
/                         # Ana sayfa
/books/                   # Kitap listesi
/books/<id>/              # Kitap detay
/books/<id>/read/         # Kitap okuma
/books/<id>/chapter/<ch>/ # Bölüm okuma
/categories/              # Kategoriler
/my-library/              # Kitaplığım
```

### Kullanıcı
```
/login/                   # Giriş
/register/                # Kayıt
/logout/                  # Çıkış
/profile/                 # Profil
/password-reset/          # Şifre sıfırlama
```

### Yazar
```
/author/dashboard/        # Yazar paneli
/author/upload/           # Kitap yükleme
/author/books/            # Yazarın kitapları
/author/edit/<id>/        # Kitap düzenle
```

### Admin Panel
```
/admin-panel/             # Dashboard
/admin-panel/books/       # Kitap yönetimi
/admin-panel/authors/     # Yazar onayları
/admin-panel/users/       # Kullanıcılar
/admin-panel/categories/  # Kategoriler
/admin-panel/premium/     # Premium yönetimi
/admin-panel/statistics/  # İstatistikler
/admin-panel/settings/    # Site ayarları ★
```

### Django Admin
```
/admin/                   # Django admin
```

---

## 🎨 Template Kullanımı

### Base Template Kullanma
```django
{% extends 'frontend/base.html' %}

{% block title %}Sayfa Başlığı{% endblock %}

{% block content %}
    <h1>İçerik buraya</h1>
{% endblock %}

{% block extra_css %}
    <style>...</style>
{% endblock %}

{% block extra_js %}
    <script>...</script>
{% endblock %}
```

### Site Ayarlarına Erişim
```django
{# Context processor sayesinde her template'de kullanılabilir #}
{{ site_settings.site_name }}
{{ site_settings.logo.url }}
{{ site_settings.contact_email }}
{{ site_settings.footer_text }}
{{ site_settings.facebook_url }}

{# Koşullu kullanım #}
{% if site_settings.logo %}
    <img src="{{ site_settings.logo.url }}" alt="{{ site_settings.site_name }}">
{% else %}
    <h1>{{ site_settings.site_name }}</h1>
{% endif %}
```

### Kullanıcı Bilgilerine Erişim
```django
{% if user.is_authenticated %}
    <p>Merhaba, {{ user.username }}!</p>
    
    {% if user.is_premium %}
        <span class="badge">Premium</span>
    {% endif %}
    
    {% if user.is_author %}
        <a href="{% url 'author_dashboard' %}">Yazar Paneli</a>
    {% endif %}
    
    {% if user.is_admin_user %}
        <a href="{% url 'admin_dashboard' %}">Admin Panel</a>
    {% endif %}
{% else %}
    <a href="{% url 'login' %}">Giriş Yap</a>
{% endif %}
```

### URL Kullanımı
```django
{# Basit URL #}
<a href="{% url 'home' %}">Ana Sayfa</a>

{# Parametreli URL #}
<a href="{% url 'book_detail' book.id %}">Kitap Detay</a>
<a href="{% url 'chapter_read' book.id chapter.id %}">Bölümü Oku</a>

{# Named arguments #}
<a href="{% url 'chapter_read' book_id=book.id chapter_id=chapter.id %}">Bölüm</a>
```

---

## 🔐 Decorator Kullanımı

### Views'de Decorator
```python
from django.contrib.auth.decorators import login_required
from main.decorators import author_required, admin_required, premium_required

# Sadece giriş yapmış kullanıcılar
@login_required
def my_view(request):
    pass

# Sadece yazarlar
@login_required
@author_required
def author_view(request):
    pass

# Sadece adminler
@login_required
@admin_required
def admin_view(request):
    pass

# Sadece premium üyeler
@login_required
@premium_required
def premium_view(request):
    pass

# Kitap sahibi veya admin
from main.decorators import book_owner_or_admin
@login_required
@book_owner_or_admin
def edit_book(request, book_id):
    pass
```

### Çoklu Decorator
```python
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

@login_required
@author_required
@require_POST
def upload_book(request):
    pass
```

---

## 📊 Model Kullanımı

### Book Model
```python
from main.models import Book, Chapter, Category

# Yeni kitap oluştur
book = Book.objects.create(
    title="Kitap Adı",
    slug="kitap-adi",
    author=request.user,
    category=category,
    description="Açıklama",
    status='draft'
)

# Kitap sorgula
book = Book.objects.get(id=1)
books = Book.objects.filter(status='published')
books = Book.objects.filter(author=user, status='published')

# İlişkili nesneler
chapters = book.chapters.all()  # Kitabın bölümleri
ratings = book.ratings.all()    # Kitabın değerlendirmeleri
avg_rating = book.average_rating()  # Ortalama puan

# Kitap güncelle
book.status = 'published'
book.views += 1
book.save()
```

### User Model
```python
from users.models import CustomUser

# Kullanıcı oluştur
user = CustomUser.objects.create_user(
    username='john',
    email='john@example.com',
    password='password123',
    role='reader'
)

# Kullanıcı sorgula
user = CustomUser.objects.get(username='john')
authors = CustomUser.objects.filter(role='author', is_author_approved=True)
premium_users = CustomUser.objects.filter(is_premium=True)

# Kullanıcı kontrolleri
if user.is_author():
    print("Yazar")
if user.is_admin_user():
    print("Admin")
if user.can_view_summaries():
    print("Özet görebilir")

# Premium üyelik
user.upgrade_to_premium()
if user.is_premium_active():
    print("Premium aktif")
```

### SiteSettings Model
```python
from main.models import SiteSettings

# Ayarları al (singleton)
settings = SiteSettings.get_settings()

# Ayarları oku
site_name = settings.site_name
logo = settings.logo.url if settings.logo else None
is_maintenance = settings.maintenance_mode

# Ayarları güncelle
settings.site_name = "Yeni İsim"
settings.maintenance_mode = True
settings.save()
```

### Category Model
```python
from main.models import Category

# Kategori oluştur
category = Category.objects.create(
    name="Roman",
    slug="roman",
    description="Roman kitapları"
)

# Kategorideki kitaplar
books = category.books.all()
```

---

## 🤖 AI Processor Kullanımı

### Dosya İşleme
```python
from main.ai_processor import process_book_file

# Kitap dosyasını işle
result = process_book_file(
    file_path=book.file.path,
    use_ai=True  # AI özeti oluştur
)

# Sonuçlar
book.summary = result['summary']
book.save()

for chapter_data in result['chapters']:
    Chapter.objects.create(
        book=book,
        title=chapter_data['title'],
        content=chapter_data['content'],
        summary=chapter_data['summary'],
        order=chapter_data['order']
    )
```

### Manuel AI Kullanımı
```python
from main.ai_processor import AIContentGenerator

generator = AIContentGenerator()

# Özet oluştur
summary = generator.generate_book_summary(
    book_content="Kitap metni...",
    book_title="Kitap Başlığı"
)

# Bölüm özeti
chapter_summary = generator._generate_ai_summary(
    text="Bölüm metni...",
    max_length=200
)
```

---

## 📝 Form Kullanımı

### Form Oluşturma
```python
from django import forms
from main.models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'category', 'cover_image', 'file']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
```

### View'de Form Kullanma
```python
def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.author = request.user
            book.status = 'draft'
            book.save()
            
            messages.success(request, 'Kitap başarıyla yüklendi!')
            return redirect('author_dashboard')
    else:
        form = BookForm()
    
    return render(request, 'author/upload_book.html', {'form': form})
```

### Template'de Form
```django
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    
    {{ form.as_p }}
    
    {# Veya manuel #}
    <div class="form-group">
        <label>{{ form.title.label }}</label>
        {{ form.title }}
        {% if form.title.errors %}
            <span class="error">{{ form.title.errors }}</span>
        {% endif %}
    </div>
    
    <button type="submit">Kaydet</button>
</form>
```

---

## 🔍 Query Optimizasyonu

### Select Related (ForeignKey)
```python
# Kötü: N+1 sorgu problemi
books = Book.objects.all()
for book in books:
    print(book.author.username)  # Her kitap için yeni sorgu

# İyi: Tek sorgu
books = Book.objects.select_related('author', 'category').all()
for book in books:
    print(book.author.username)  # Sorgu yok
```

### Prefetch Related (ManyToMany, Reverse FK)
```python
# Kötü
books = Book.objects.all()
for book in books:
    for chapter in book.chapters.all():  # Her kitap için yeni sorgu
        print(chapter.title)

# İyi
books = Book.objects.prefetch_related('chapters').all()
for book in books:
    for chapter in book.chapters.all():  # Sorgu yok
        print(chapter.title)
```

### Aggregate ve Annotate
```python
from django.db.models import Count, Avg

# Kitap sayısı ile kategoriler
categories = Category.objects.annotate(
    book_count=Count('books')
).filter(book_count__gt=0)

# Ortalama puan
from django.db.models import Avg
book = Book.objects.annotate(
    avg_rating=Avg('ratings__rating')
).get(id=1)
```

---

## ⚙️ Ayarlar (settings.py)

### Geliştirme vs Production
```python
# settings.py

DEBUG = True  # Production'da False

# Production için
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Security
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
```

### Database
```python
# Geliştirme (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Production (PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'librovaai_db',
        'USER': 'dbuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Email
```python
# Console backend (geliştirme)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SMTP (production)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = 'Librovaai <noreply@librovaai.com>'
```

---

## 🐛 Debugging İpuçları

### Print Debugging
```python
# View'de
def my_view(request):
    print(f"User: {request.user}")
    print(f"Method: {request.method}")
    print(f"POST data: {request.POST}")
    print(f"FILES: {request.FILES}")
```

### Django Debug Toolbar
```bash
pip install django-debug-toolbar
```

```python
# settings.py
INSTALLED_APPS += ['debug_toolbar']
MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
INTERNAL_IPS = ['127.0.0.1']

# urls.py
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
```

### Logging
```python
# settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

```python
# View'de kullanım
import logging
logger = logging.getLogger(__name__)

def my_view(request):
    logger.debug('Bu bir debug mesajı')
    logger.info('Bu bir info mesajı')
    logger.warning('Bu bir warning mesajı')
    logger.error('Bu bir error mesajı')
```

---

## 🚀 Production Checklist

### Pre-deployment
- [ ] `DEBUG = False`
- [ ] `ALLOWED_HOSTS` ayarlandı
- [ ] Secret key güvenli
- [ ] Database production'a hazır (PostgreSQL)
- [ ] Static files collect edildi: `python manage.py collectstatic`
- [ ] Migration'lar uygulandı
- [ ] Test'ler geçti
- [ ] Requirements.txt güncellendi

### Security
- [ ] HTTPS etkin
- [ ] SECURE_SSL_REDIRECT = True
- [ ] SESSION_COOKIE_SECURE = True
- [ ] CSRF_COOKIE_SECURE = True
- [ ] SECURE_HSTS_SECONDS ayarlandı

### Performance
- [ ] Database indeksleri eklendi
- [ ] Gunicorn/uWSGI kuruldu
- [ ] Nginx reverse proxy yapılandırıldı
- [ ] Redis cache (opsiyonel)
- [ ] CDN için static files (opsiyonel)

---

## 📚 Yararlı Kaynaklar

### Dokümantasyon
- [Django Docs](https://docs.djangoproject.com/)
- [Django Best Practices](https://django-best-practices.readthedocs.io/)
- PROJECT_DOCUMENTATION.md
- SITE_SETTINGS_GUIDE.md
- ARCHITECTURE.md

### Kodda Arama
```bash
# Tüm projede ara
grep -r "search_term" .

# Python dosyalarında ara
grep -r "search_term" --include="*.py"

# Model ara
grep -r "class Book" --include="*.py"
```

### Git
```bash
# Değişiklikleri gör
git status
git diff

# Commit
git add .
git commit -m "Mesaj"

# Push
git push origin main
```

---

## 💡 Hızlı Kod Snippets

### Pagination
```python
from django.core.paginator import Paginator

def book_list(request):
    books = Book.objects.filter(status='published')
    paginator = Paginator(books, 12)  # 12 kitap per sayfa
    page = request.GET.get('page', 1)
    books = paginator.get_page(page)
    return render(request, 'books_list.html', {'books': books})
```

### Messages
```python
from django.contrib import messages

messages.success(request, 'İşlem başarılı!')
messages.error(request, 'Bir hata oluştu!')
messages.warning(request, 'Dikkat!')
messages.info(request, 'Bilgi mesajı')
```

### File Upload
```python
def handle_uploaded_file(f):
    with open(f'media/books/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
```

---

**⚡ Hızlı Erişim:** Bu dosyayı favorilerinize ekleyin!  
**🔖 Kısayol:** Ctrl+F ile arama yapabilirsiniz  
**📅 Güncellenme:** 2024
