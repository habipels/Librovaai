from django.contrib import admin
from .models import Article, ArticleSeries, Book, Chapter, Category, BookRating, ReadingProgress, Bookmark, SiteSettings

# ==================== MEVCUT ARTICLE SİSTEMİ ====================

class ArticleSeriesAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'subtitle',
        'slug',
        'author',
        'image',
        # 'published'
    ]

class ArticleAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Header", {"fields": ['title', 'subtitle', 'article_slug', 'series', 'author', 'image']}),
        ("Content", {"fields": ['content', 'notes']}),
        ("Date", {"fields": ['modified']})
    ]

admin.site.register(ArticleSeries, ArticleSeriesAdmin)
admin.site.register(Article, ArticleAdmin)


# ==================== KİTAP SİSTEMİ ====================

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'status', 'view_count', 'created_at']
    list_filter = ['status', 'created_at', 'is_processed']
    search_fields = ['title', 'author__username', 'isbn']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['categories']
    
    fieldsets = [
        ('Temel Bilgiler', {
            'fields': ['title', 'slug', 'subtitle', 'description', 'author', 'categories']
        }),
        ('Dosyalar', {
            'fields': ['file', 'file_type', 'cover_image']
        }),
        ('Durum', {
            'fields': ['status', 'is_processed', 'has_toc']
        }),
        ('AI Bilgileri', {
            'fields': ['ai_summary'],
            'classes': ['collapse']
        }),
        ('Yayıncı Bilgileri', {
            'fields': ['publisher', 'isbn', 'publication_year', 'page_count', 'language'],
            'classes': ['collapse']
        }),
        ('İstatistikler', {
            'fields': ['view_count', 'download_count'],
            'classes': ['collapse']
        }),
        ('Admin Notları', {
            'fields': ['admin_notes', 'rejection_reason'],
            'classes': ['collapse']
        }),
    ]


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'chapter_number', 'level', 'order']
    list_filter = ['book', 'level']
    search_fields = ['title', 'book__title']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(BookRating)
class BookRatingAdmin(admin.ModelAdmin):
    list_display = ['book', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['book__title', 'user__username']


@admin.register(ReadingProgress)
class ReadingProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'progress_percentage', 'last_read_at']
    list_filter = ['last_read_at']
    search_fields = ['user__username', 'book__title']


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'chapter', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'book__title']


# ========================== SİSTEM AYARLARI ==========================

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Site Ayarları Admin
    Singleton pattern - Sadece düzenleme yapılabilir
    """
    
    fieldsets = [
        ('Temel Bilgiler', {
            'fields': ['site_name', 'site_description', 'site_keywords']
        }),
        ('Görseller', {
            'fields': ['site_logo', 'site_favicon']
        }),
        ('İletişim Bilgileri', {
            'fields': ['contact_email', 'contact_phone', 'contact_address']
        }),
        ('Sosyal Medya', {
            'fields': ['facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'],
            'classes': ['collapse']
        }),
        ('Footer', {
            'fields': ['footer_text', 'footer_about'],
            'classes': ['collapse']
        }),
        ('SEO', {
            'fields': ['meta_title', 'meta_description', 'google_analytics_id', 'google_site_verification'],
            'classes': ['collapse']
        }),
        ('Sistem Ayarları', {
            'fields': ['maintenance_mode', 'maintenance_message', 'default_language', 'timezone'],
        }),
        ('Özellik Ayarları', {
            'fields': ['allow_registration', 'allow_comments', 'enable_ai_processing'],
            'classes': ['collapse']
        }),
    ]
    
    def has_add_permission(self, request):
        """Yeni kayıt eklemeyi engelle (singleton)"""
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Silmeyi engelle"""
        return False
