from django.db import models
from django.utils import timezone
from tinymce.models import HTMLField
from django.contrib.auth import get_user_model

from django.template.defaultfilters import slugify
import os

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


class SiteSettings(models.Model):
    """
    Site ayarları modeli - Singleton pattern kullanır (tek kayıt)
    Logo, iletişim bilgileri, sosyal medya linkleri vb.
    """
    def logo_upload_to(self, instance=None):
        if instance:
            return os.path.join("site_settings", "logo", instance)
        return None
    
    def favicon_upload_to(self, instance=None):
        if instance:
            return os.path.join("site_settings", "favicon", instance)
        return None
    
    def banner_upload_to(self, instance=None):
        if instance:
            return os.path.join("site_settings", "banners", instance)
        return None

    # Temel Bilgiler
    site_name = models.CharField("Site Adı", max_length=200, default="Libraria")
    site_description = models.TextField("Site Açıklaması", max_length=500, default="", blank=True)
    site_keywords = models.CharField("SEO Anahtar Kelimeler", max_length=500, default="", blank=True)
    logo = models.ImageField("Logo", upload_to=logo_upload_to, blank=True, null=True)
    favicon = models.ImageField("Favicon", upload_to=favicon_upload_to, blank=True, null=True)
    
    # İletişim Bilgileri
    contact_email = models.EmailField("İletişim Email", max_length=100, default="", blank=True)
    contact_phone = models.CharField("Telefon", max_length=20, default="", blank=True)
    contact_address = models.TextField("Adres", max_length=500, default="", blank=True)
    
    # Sosyal Medya
    facebook_url = models.URLField("Facebook", max_length=200, default="", blank=True)
    twitter_url = models.URLField("Twitter/X", max_length=200, default="", blank=True)
    instagram_url = models.URLField("Instagram", max_length=200, default="", blank=True)
    linkedin_url = models.URLField("LinkedIn", max_length=200, default="", blank=True)
    youtube_url = models.URLField("YouTube", max_length=200, default="", blank=True)
    
    # Footer
    footer_text = models.CharField("Footer Metni", max_length=200, default="", blank=True)
    footer_about = models.TextField("Footer Hakkımızda", max_length=1000, default="", blank=True)
    
    # Banner / Slider Ayarları
    banner_image_1 = models.ImageField("Banner Görseli 1", upload_to=banner_upload_to, blank=True, null=True)
    banner_title_1 = models.CharField("Banner Başlık 1", max_length=200, default="Online Learning Anytime, Anywhere!", blank=True)
    banner_subtitle_1 = models.CharField("Banner Alt Başlık 1", max_length=200, default="Discover Your Roots", blank=True)
    banner_description_1 = models.TextField("Banner Açıklama 1", max_length=500, default="", blank=True)
    banner_button_text_1 = models.CharField("Banner Buton Metni 1", max_length=50, default="Read More", blank=True)
    banner_button_link_1 = models.CharField("Banner Buton Linki 1", max_length=200, default="#", blank=True)
    
    banner_image_2 = models.ImageField("Banner Görseli 2", upload_to=banner_upload_to, blank=True, null=True)
    banner_title_2 = models.CharField("Banner Başlık 2", max_length=200, default="", blank=True)
    banner_subtitle_2 = models.CharField("Banner Alt Başlık 2", max_length=200, default="", blank=True)
    banner_description_2 = models.TextField("Banner Açıklama 2", max_length=500, default="", blank=True)
    banner_button_text_2 = models.CharField("Banner Buton Metni 2", max_length=50, default="", blank=True)
    banner_button_link_2 = models.CharField("Banner Buton Linki 2", max_length=200, default="#", blank=True)
    
    banner_image_3 = models.ImageField("Banner Görseli 3", upload_to=banner_upload_to, blank=True, null=True)
    banner_title_3 = models.CharField("Banner Başlık 3", max_length=200, default="", blank=True)
    banner_subtitle_3 = models.CharField("Banner Alt Başlık 3", max_length=200, default="", blank=True)
    banner_description_3 = models.TextField("Banner Açıklama 3", max_length=500, default="", blank=True)
    banner_button_text_3 = models.CharField("Banner Buton Metni 3", max_length=50, default="", blank=True)
    banner_button_link_3 = models.CharField("Banner Buton Linki 3", max_length=200, default="#", blank=True)
    
    enable_banner = models.BooleanField("Banner/Slider Aktif", default=True)
    
    # SEO
    meta_title = models.CharField("Meta Title", max_length=200, default="", blank=True)
    meta_description = models.TextField("Meta Description", max_length=500, default="", blank=True)
    google_analytics_id = models.CharField("Google Analytics ID", max_length=50, default="", blank=True)
    
    # Sistem Ayarları
    maintenance_mode = models.BooleanField("Bakım Modu", default=False)
    maintenance_message = models.TextField("Bakım Modu Mesajı", max_length=500, default="Site bakımda, lütfen daha sonra tekrar deneyin.", blank=True)
    default_language = models.CharField("Varsayılan Dil", max_length=10, default="tr")
    timezone = models.CharField("Zaman Dilimi", max_length=50, default="Europe/Istanbul")
    
    # Özellikler
    allow_registration = models.BooleanField("Kayıt İzni", default=True)
    allow_comments = models.BooleanField("Yorum İzni", default=True)
    enable_ai_processing = models.BooleanField("AI İşleme Aktif", default=False)
    
    created_at = models.DateTimeField("Oluşturulma", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme", auto_now=True)

    class Meta:
        verbose_name = "Site Ayarı"
        verbose_name_plural = "Site Ayarları"

    def __str__(self):
        return f"{self.site_name} - Site Ayarları"

    @classmethod
    def get_settings(cls):
        """Singleton pattern - tek bir ayar kaydı döndürür"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings

    def save(self, *args, **kwargs):
        """Singleton pattern - sadece 1 kayıt olabilir"""
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Singleton pattern - kayıt silinemez"""
        pass


class BookCategory(models.Model):
    """
    Kitap kategorileri - Admin tarafından yönetilir
    """
    name = models.CharField("Kategori Adı", max_length=100, unique=True)
    slug = models.SlugField("Slug", max_length=120, unique=True, blank=True)
    description = models.TextField("Açıklama", max_length=500, blank=True)
    icon = models.CharField("İkon (Font Awesome)", max_length=50, blank=True, help_text="Örn: fa-book, fa-science")
    color = models.CharField("Renk Kodu", max_length=7, default="#3498db", help_text="Hex renk kodu (örn: #3498db)")
    
    # Sıralama ve görünürlük
    order = models.IntegerField("Sıralama", default=0)
    is_active = models.BooleanField("Aktif", default=True)
    
    # İstatistikler
    book_count = models.IntegerField("Kitap Sayısı", default=0, editable=False)
    
    created_at = models.DateTimeField("Oluşturulma", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme", auto_now=True)
    
    class Meta:
        verbose_name = "Kitap Kategorisi"
        verbose_name_plural = "Kitap Kategorileri"
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def update_book_count(self):
        """Kategorideki kitap sayısını günceller"""
        self.book_count = self.books.filter(status='published').count()
        self.save(update_fields=['book_count'])


class Book(models.Model):
    """
    Kitap modeli - Yazarlar tarafından yüklenir, admin onayı ile yayınlanır
    """
    STATUS_CHOICES = (
        ('draft', 'Taslak'),
        ('pending', 'Onay Bekliyor'),
        ('approved', 'Onaylandı'),
        ('published', 'Yayında'),
        ('rejected', 'Reddedildi'),
        ('archived', 'Arşivlendi'),
    )
    
    def cover_upload_to(self, instance=None):
        if instance:
            return os.path.join("Books", "covers", str(self.id), instance)
        return None
    
    def file_upload_to(self, instance=None):
        if instance:
            return os.path.join("Books", "files", str(self.id), instance)
        return None
    
    # Temel Bilgiler
    title = models.CharField("Kitap Başlığı", max_length=300)
    slug = models.SlugField("Slug", max_length=350, unique=True, blank=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='books', verbose_name="Yazar")
    co_authors = models.ManyToManyField(get_user_model(), related_name='co_authored_books', blank=True, verbose_name="Ortak Yazarlar")
    
    # İçerik
    description = models.TextField("Açıklama", max_length=2000, help_text="Kitap hakkında kısa açıklama")
    isbn = models.CharField("ISBN", max_length=13, blank=True, unique=True, null=True)
    publisher = models.CharField("Yayınevi", max_length=200, blank=True)
    language = models.CharField("Dil", max_length=10, default='tr')
    page_count = models.IntegerField("Sayfa Sayısı", default=0, blank=True)
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='books', verbose_name="Kategori")
    tags = models.CharField("Etiketler", max_length=500, blank=True, help_text="Virgülle ayırın")
    
    # Dosyalar
    cover_image = models.ImageField("Kapak Resmi", upload_to=cover_upload_to, blank=True, null=True)
    file = models.FileField("Kitap Dosyası (PDF/Word)", upload_to=file_upload_to, blank=True, null=True)
    file_type = models.CharField("Dosya Tipi", max_length=10, blank=True)  # pdf, docx, doc
    file_size = models.BigIntegerField("Dosya Boyutu (bytes)", default=0, blank=True)
    
    # AI İşleme
    is_processed = models.BooleanField("AI İşlendi", default=False)
    has_toc = models.BooleanField("İçindekiler Var", default=False)
    has_summary = models.BooleanField("Özet Var", default=False)
    processing_error = models.TextField("İşleme Hatası", blank=True)
    
    # Durum
    status = models.CharField("Durum", max_length=20, choices=STATUS_CHOICES, default='draft')
    rejection_reason = models.TextField("Red Nedeni", blank=True)
    
    # Tarihler
    created_at = models.DateTimeField("Oluşturulma", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme", auto_now=True)
    published_at = models.DateTimeField("Yayın Tarihi", null=True, blank=True)
    approved_by = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_books', verbose_name="Onaylayan Admin")
    
    # İstatistikler
    view_count = models.IntegerField("Görüntülenme", default=0)
    download_count = models.IntegerField("İndirme", default=0)
    rating_count = models.IntegerField("Değerlendirme Sayısı", default=0)
    rating_average = models.DecimalField("Ortalama Puan", max_digits=3, decimal_places=2, default=0.00)
    
    class Meta:
        verbose_name = "Kitap"
        verbose_name_plural = "Kitaplar"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.author.username}"
    
    def save(self, *args, **kwargs):
        # Slug oluştur
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
            # Eğer aynı slug varsa, ID ekle
            if Book.objects.filter(slug=self.slug).exists():
                self.slug = f"{self.slug}-{timezone.now().timestamp()}"
        
        # Dosya tipini belirle
        if self.file:
            file_ext = self.file.name.split('.')[-1].lower()
            self.file_type = file_ext
            self.file_size = self.file.size
        
        super().save(*args, **kwargs)
    
    @property
    def is_published(self):
        return self.status == 'published'
    
    @property
    def can_be_read(self):
        return self.status in ['published', 'approved']


class Chapter(models.Model):
    """
    Kitap bölümleri - AI tarafından otomatik oluşturulur veya manuel eklenir
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters', verbose_name="Kitap")
    
    # Bölüm bilgileri
    title = models.CharField("Bölüm Başlığı", max_length=500)
    slug = models.SlugField("Slug", max_length=550, blank=True)
    order = models.IntegerField("Sıra", default=0, help_text="Bölüm sırası")
    
    # İçerik
    content = HTMLField("İçerik", blank=True)
    page_start = models.IntegerField("Başlangıç Sayfası", default=0, blank=True)
    page_end = models.IntegerField("Bitiş Sayfası", default=0, blank=True)
    word_count = models.IntegerField("Kelime Sayısı", default=0, blank=True)
    
    # Hiyerarşi (ana bölüm / alt bölüm)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subchapters', verbose_name="Üst Bölüm")
    level = models.IntegerField("Seviye", default=1, help_text="1=Ana Bölüm, 2=Alt Bölüm")
    
    # Meta
    created_at = models.DateTimeField("Oluşturulma", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme", auto_now=True)
    
    class Meta:
        verbose_name = "Bölüm"
        verbose_name_plural = "Bölümler"
        ordering = ['book', 'order']
        unique_together = ['book', 'order']
    
    def __str__(self):
        return f"{self.book.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BookSummary(models.Model):
    """
    AI tarafından oluşturulan kitap özetleri - Sadece premium üyeler görebilir
    """
    SUMMARY_TYPE_CHOICES = (
        ('short', 'Kısa Özet'),
        ('medium', 'Orta Özet'),
        ('detailed', 'Detaylı Özet'),
        ('chapter', 'Bölüm Özeti'),
    )
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='summaries', verbose_name="Kitap")
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, null=True, blank=True, related_name='summary', verbose_name="Bölüm")
    
    summary_type = models.CharField("Özet Tipi", max_length=20, choices=SUMMARY_TYPE_CHOICES, default='medium')
    content = models.TextField("Özet İçeriği")
    
    # AI bilgileri
    generated_by = models.CharField("Oluşturan AI", max_length=50, default='OpenAI', help_text="OpenAI, Gemini, vb.")
    generated_at = models.DateTimeField("Oluşturulma", auto_now_add=True)
    token_count = models.IntegerField("Token Sayısı", default=0, blank=True)
    
    # Erişim kontrolü
    is_premium_only = models.BooleanField("Sadece Premium", default=True)
    
    # Meta
    word_count = models.IntegerField("Kelime Sayısı", default=0, blank=True)
    
    class Meta:
        verbose_name = "Kitap Özeti"
        verbose_name_plural = "Kitap Özetleri"
        unique_together = ['book', 'summary_type', 'chapter']
    
    def __str__(self):
        if self.chapter:
            return f"{self.book.title} - {self.chapter.title} Özeti"
        return f"{self.book.title} - {self.get_summary_type_display()}"
    
    def save(self, *args, **kwargs):
        # Kelime sayısını hesapla
        if self.content:
            self.word_count = len(self.content.split())
        super().save(*args, **kwargs)