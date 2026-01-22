from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model
from django.template.defaultfilters import slugify
import os

# ========================== ARTICLE MODELLER (Mevcut) ==========================

class ArticleSeries(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("ArticleSeries", slugify(self.slug), instance)
        return None

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="", blank=True) 
    slug = models.SlugField("Series slug", null=False, blank=False, unique=True)
    published = models.DateTimeField("Date published", default=timezone.now)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    image = models.ImageField(default='default/no_image.jpg', upload_to=image_upload_to ,max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Series"
        ordering = ['-published']

class Article(models.Model):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("ArticleSeries", slugify(self.series.slug), slugify(self.article_slug), instance)
        return None

    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200, default="", blank=True)
    article_slug = models.SlugField("Article slug", null=False, blank=False, unique=True)
    content = HTMLField(blank=True, default="")
    notes = HTMLField(blank=True, default="")
    published = models.DateTimeField("Date published", default=timezone.now)
    modified = models.DateTimeField("Date modified", default=timezone.now)
    series = models.ForeignKey(ArticleSeries, default="", verbose_name="Series", on_delete=models.SET_DEFAULT)
    author = models.ForeignKey(get_user_model(), default=1, on_delete=models.SET_DEFAULT)
    image = models.ImageField(default='default/no_image.jpg', upload_to=image_upload_to ,max_length=255)

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return self.series.slug + "/" + self.article_slug

    class Meta:
        verbose_name_plural = "Article"
        ordering = ['-published']


# ========================== KİTAP SİSTEMİ MODELLERİ ==========================

class Category(models.Model):
    """Kitap Kategorileri"""
    name = models.CharField("Kategori Adı", max_length=100, unique=True)
    slug = models.SlugField("Kategori Slug", unique=True)
    description = models.TextField("Açıklama", blank=True)
    created_at = models.DateTimeField("Oluşturma Tarihi", auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategoriler"
        ordering = ['name']


class Book(models.Model):
    """Kitap Modeli"""
    
    STATUS_CHOICES = (
        ('draft', 'Taslak'),
        ('pending', 'Onay Bekliyor'),
        ('approved', 'Onaylandı'),
        ('published', 'Yayında'),
        ('rejected', 'Reddedildi'),
    )
    
    FILE_TYPE_CHOICES = (
        ('pdf', 'PDF'),
        ('docx', 'Word (DOCX)'),
        ('doc', 'Word (DOC)'),
    )
    
    def book_upload_to(self, filename):
        return os.path.join("Books", slugify(self.slug), filename)
    
    def cover_upload_to(self, filename):
        return os.path.join("BookCovers", slugify(self.slug), filename)
    
    # Temel Bilgiler
    title = models.CharField("Kitap Başlığı", max_length=300)
    slug = models.SlugField("Slug", unique=True, max_length=350)
    subtitle = models.CharField("Alt Başlık", max_length=300, blank=True)
    description = models.TextField("Açıklama", blank=True)
    author = models.ForeignKey(
        get_user_model(), 
        on_delete=models.CASCADE, 
        related_name='books',
        verbose_name="Yazar"
    )
    
    # Kategoriler
    categories = models.ManyToManyField(Category, related_name='books', verbose_name="Kategoriler")
    
    # Dosya ve Görsel
    file = models.FileField("Kitap Dosyası", upload_to=book_upload_to, blank=True, null=True)
    file_type = models.CharField("Dosya Tipi", max_length=10, choices=FILE_TYPE_CHOICES, blank=True)
    cover_image = models.ImageField("Kapak Görseli", upload_to=cover_upload_to, default='default/book_cover.jpg')
    
    # Durum ve Onay
    status = models.CharField("Durum", max_length=20, choices=STATUS_CHOICES, default='draft')
    is_processed = models.BooleanField("İşlendi mi?", default=False, help_text="Dosya AI tarafından işlendi mi?")
    
    # AI İşlemleri
    ai_summary = models.TextField("AI Özeti", blank=True, help_text="AI tarafından oluşturulan özet")
    has_toc = models.BooleanField("İçindekiler var mı?", default=False)
    
    # İstatistikler
    view_count = models.IntegerField("Görüntülenme", default=0)
    download_count = models.IntegerField("İndirilme", default=0)
    
    # Tarihler
    created_at = models.DateTimeField("Oluşturma Tarihi", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme Tarihi", auto_now=True)
    published_at = models.DateTimeField("Yayın Tarihi", blank=True, null=True)
    
    # Yayıncı Bilgileri
    publisher = models.CharField("Yayınevi", max_length=200, blank=True)
    isbn = models.CharField("ISBN", max_length=20, blank=True, unique=True, null=True)
    publication_year = models.IntegerField("Yayın Yılı", blank=True, null=True)
    page_count = models.IntegerField("Sayfa Sayısı", blank=True, null=True)
    language = models.CharField("Dil", max_length=50, default="Türkçe")
    
    # Admin Notları
    admin_notes = models.TextField("Admin Notları", blank=True)
    rejection_reason = models.TextField("Red Nedeni", blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.author.username}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Yayın tarihi otomatik set et
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Kitap"
        verbose_name_plural = "Kitaplar"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['slug']),
        ]


class Chapter(models.Model):
    """Kitap Bölümleri"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters', verbose_name="Kitap")
    title = models.CharField("Bölüm Başlığı", max_length=500)
    slug = models.SlugField("Slug", max_length=550)
    content = models.TextField("İçerik", blank=True)
    
    # Hiyerarşi
    chapter_number = models.IntegerField("Bölüm Numarası", default=1)
    level = models.IntegerField("Seviye", default=1, help_text="1: Ana başlık, 2: Alt başlık, vb.")
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='subchapters',
        verbose_name="Üst Bölüm"
    )
    
    # Pozisyon (sıralama)
    order = models.IntegerField("Sıra", default=0)
    
    # Sayfa bilgisi
    page_start = models.IntegerField("Başlangıç Sayfası", blank=True, null=True)
    page_end = models.IntegerField("Bitiş Sayfası", blank=True, null=True)
    
    # AI Özeti
    ai_summary = models.TextField("Bölüm Özeti", blank=True)
    
    created_at = models.DateTimeField("Oluşturma Tarihi", auto_now_add=True)
    
    def __str__(self):
        return f"{self.book.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Bölüm"
        verbose_name_plural = "Bölümler"
        ordering = ['book', 'order', 'chapter_number']
        unique_together = [['book', 'slug']]


class BookRating(models.Model):
    """Kitap Değerlendirme"""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings', verbose_name="Kitap")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Kullanıcı")
    rating = models.IntegerField("Puan", choices=[(i, i) for i in range(1, 6)])
    review = models.TextField("Yorum", blank=True)
    created_at = models.DateTimeField("Tarih", auto_now_add=True)
    
    def __str__(self):
        return f"{self.book.title} - {self.user.username}: {self.rating}/5"
    
    class Meta:
        verbose_name = "Değerlendirme"
        verbose_name_plural = "Değerlendirmeler"
        unique_together = [['book', 'user']]
        ordering = ['-created_at']


class ReadingProgress(models.Model):
    """Okuma İlerlemesi"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Kullanıcı")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Kitap")
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Son Okunan Bölüm")
    progress_percentage = models.IntegerField("İlerleme %", default=0)
    last_read_at = models.DateTimeField("Son Okuma", auto_now=True)
    started_at = models.DateTimeField("Başlangıç", auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}: %{self.progress_percentage}"
    
    class Meta:
        verbose_name = "Okuma İlerlemesi"
        verbose_name_plural = "Okuma İlerlemeleri"
        unique_together = [['user', 'book']]
        ordering = ['-last_read_at']


class Bookmark(models.Model):
    """Yer İmleri"""
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Kullanıcı")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Kitap")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name="Bölüm")
    note = models.TextField("Not", blank=True)
    created_at = models.DateTimeField("Tarih", auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.book.title}"
    
    class Meta:
        verbose_name = "Yer İmi"
        verbose_name_plural = "Yer İmleri"
        ordering = ['-created_at']


# ========================== SİSTEM AYARLARI ==========================

class SiteSettings(models.Model):
    """
    Site Genel Ayarları
    Singleton pattern - Sadece 1 kayıt olmalı
    """
    
    # Temel Bilgiler
    site_name = models.CharField("Site Adı", max_length=100, default="Librovaai")
    site_description = models.TextField("Site Açıklaması", default="Dijital Kitap Platformu", max_length=500)
    site_keywords = models.CharField("SEO Anahtar Kelimeler", max_length=500, blank=True)
    
    # Görseller
    site_logo = models.ImageField("Site Logosu", upload_to="settings/", blank=True, null=True)
    site_favicon = models.ImageField("Favicon", upload_to="settings/", blank=True, null=True)
    
    # İletişim Bilgileri
    contact_email = models.EmailField("İletişim E-posta", default="info@librovaai.com")
    contact_phone = models.CharField("Telefon", max_length=20, blank=True)
    contact_address = models.TextField("Adres", blank=True)
    
    # Sosyal Medya
    facebook_url = models.URLField("Facebook URL", blank=True)
    twitter_url = models.URLField("Twitter URL", blank=True)
    instagram_url = models.URLField("Instagram URL", blank=True)
    linkedin_url = models.URLField("LinkedIn URL", blank=True)
    youtube_url = models.URLField("YouTube URL", blank=True)
    
    # Footer
    footer_text = models.TextField("Footer Metni", default="© 2026 Librovaai. Tüm hakları saklıdır.", max_length=500)
    footer_about = models.TextField("Footer Hakkımızda", blank=True, max_length=500)
    
    # SEO
    meta_title = models.CharField("Meta Başlık", max_length=150, default="Librovaai - Dijital Kitap Platformu")
    meta_description = models.TextField("Meta Açıklama", max_length=300, default="AI destekli dijital kitap platformu")
    
    # Sistem Ayarları
    maintenance_mode = models.BooleanField("Bakım Modu", default=False, help_text="Aktif olduğunda site ziyaretçilere kapatılır")
    maintenance_message = models.TextField("Bakım Modu Mesajı", default="Şu anda bakımdayız. Kısa süre içinde geri döneceğiz.", max_length=500)
    
    # Dil ve Bölge
    default_language = models.CharField("Varsayılan Dil", max_length=10, default="tr", choices=[
        ('tr', 'Türkçe'),
        ('en', 'English'),
        ('de', 'Deutsch'),
        ('fr', 'Français'),
    ])
    timezone = models.CharField("Zaman Dilimi", max_length=50, default="Europe/Istanbul")
    
    # Özellik Ayarları
    allow_registration = models.BooleanField("Kayıt İzni", default=True, help_text="Yeni kullanıcı kaydına izin ver")
    allow_comments = models.BooleanField("Yorum İzni", default=True, help_text="Kitap yorumlarına izin ver")
    enable_ai_processing = models.BooleanField("AI İşleme", default=False, help_text="AI özet üretimini aktif et")
    
    # Google Analytics & SEO
    google_analytics_id = models.CharField("Google Analytics ID", max_length=50, blank=True)
    google_site_verification = models.CharField("Google Site Verification", max_length=100, blank=True)
    
    # Güncelleme Bilgisi
    updated_at = models.DateTimeField("Güncellenme", auto_now=True)
    
    def __str__(self):
        return f"Site Ayarları - {self.site_name}"
    
    class Meta:
        verbose_name = "Site Ayarları"
        verbose_name_plural = "Site Ayarları"
    
    def save(self, *args, **kwargs):
        """Singleton pattern - Sadece bir kayıt olabilir"""
        if not self.pk and SiteSettings.objects.exists():
            # Eğer pk yok ve başka kayıt varsa, mevcut kaydı güncelle
            settings = SiteSettings.objects.first()
            self.pk = settings.pk
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Ayarları getir, yoksa varsayılanları oluştur"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Librovaai',
                'site_description': 'Dijital Kitap Platformu',
                'contact_email': 'info@librovaai.com',
            }
        )
        return settings