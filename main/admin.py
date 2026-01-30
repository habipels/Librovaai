from django.contrib import admin
from .models import Article, ArticleSeries, SiteSettings, Book, Chapter, BookSummary, BookCategory
from django.utils.html import format_html

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

# Register your models here.
admin.site.register(ArticleSeries, ArticleSeriesAdmin)
admin.site.register(Article, ArticleAdmin)


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Temel Bilgiler", {
            "fields": ['site_name', 'site_description', 'site_keywords', 'logo', 'favicon']
        }),
        ("İletişim Bilgileri", {
            "fields": ['contact_email', 'contact_phone', 'contact_address']
        }),
        ("Sosyal Medya", {
            "fields": ['facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url', 'youtube_url'],
            "classes": ['collapse']
        }),
        ("Footer", {
            "fields": ['footer_text', 'footer_about'],
            "classes": ['collapse']
        }),
        ("Ana Banner / Slider", {
            "fields": [
                'enable_banner',
                'banner_image_1', 'banner_title_1', 'banner_subtitle_1', 'banner_description_1', 
                'banner_button_text_1', 'banner_button_link_1',
                'banner_image_2', 'banner_title_2', 'banner_subtitle_2', 'banner_description_2',
                'banner_button_text_2', 'banner_button_link_2',
                'banner_image_3', 'banner_title_3', 'banner_subtitle_3', 'banner_description_3',
                'banner_button_text_3', 'banner_button_link_3',
            ],
            "classes": ['collapse']
        }),
        ("SEO Ayarları", {
            "fields": ['meta_title', 'meta_description', 'google_analytics_id'],
            "classes": ['collapse']
        }),
        ("Sistem Ayarları", {
            "fields": ['maintenance_mode', 'maintenance_message', 'default_language', 'timezone'],
            "classes": ['collapse']
        }),
        ("Özellikler", {
            "fields": ['allow_registration', 'allow_comments', 'enable_ai_processing'],
            "classes": ['collapse']
        }),
    ]

    def has_add_permission(self, request):
        """Singleton - sadece 1 kayıt olabilir, yeni ekleme yapılamaz"""
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        """Singleton - kayıt silinemez"""
        return False


@admin.register(BookCategory)
class BookCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'book_count', 'color_badge', 'is_active', 'order']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['book_count', 'created_at', 'updated_at']
    
    fieldsets = [
        ("Temel Bilgiler", {
            "fields": ['name', 'slug', 'description']
        }),
        ("Görünüm", {
            "fields": ['icon', 'color', 'order', 'is_active']
        }),
        ("İstatistikler", {
            "fields": ['book_count', 'created_at', 'updated_at'],
            "classes": ['collapse']
        }),
    ]
    
    def color_badge(self, obj):
        return format_html(
            '<span style="background-color: {}; color: white; padding: 5px 15px; border-radius: 3px; display: inline-block;">{}</span>',
            obj.color,
            obj.name
        )
    color_badge.short_description = 'Renk Önizleme'


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0
    fields = ['order', 'title', 'page_start', 'page_end', 'level', 'parent']
    ordering = ['order']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status_badge', 'is_processed', 'view_count', 'created_at']
    list_filter = ['status', 'category', 'is_processed', 'has_toc', 'has_summary', 'created_at']
    search_fields = ['title', 'author__username', 'isbn', 'description']
    readonly_fields = ['slug', 'created_at', 'updated_at', 'view_count', 'download_count', 
                       'file_type', 'file_size', 'is_processed', 'processing_error']
    
    fieldsets = [
        ("Temel Bilgiler", {
            "fields": ['title', 'slug', 'author', 'co_authors', 'category', 'language']
        }),
        ("İçerik", {
            "fields": ['description', 'isbn', 'publisher', 'page_count', 'tags']
        }),
        ("Dosyalar", {
            "fields": ['cover_image', 'file', 'file_type', 'file_size']
        }),
        ("Durum", {
            "fields": ['status', 'rejection_reason', 'approved_by', 'published_at']
        }),
        ("AI İşleme", {
            "fields": ['is_processed', 'has_toc', 'has_summary', 'processing_error'],
            "classes": ['collapse']
        }),
        ("İstatistikler", {
            "fields": ['view_count', 'download_count', 'rating_count', 'rating_average'],
            "classes": ['collapse']
        }),
        ("Tarihler", {
            "fields": ['created_at', 'updated_at'],
            "classes": ['collapse']
        }),
    ]
    
    inlines = [ChapterInline]
    
    actions = ['approve_books', 'publish_books', 'reject_books', 'process_with_ai']
    
    def status_badge(self, obj):
        colors = {
            'draft': 'gray',
            'pending': 'orange',
            'approved': 'green',
            'published': 'blue',
            'rejected': 'red',
            'archived': 'black',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Durum'
    
    def approve_books(self, request, queryset):
        updated = queryset.filter(status='pending').update(
            status='approved',
            approved_by=request.user
        )
        self.message_user(request, f'{updated} kitap onaylandı.')
    approve_books.short_description = 'Seçili kitapları onayla'
    
    def publish_books(self, request, queryset):
        from django.utils import timezone
        for book in queryset.filter(status__in=['approved', 'pending']):
            book.status = 'published'
            book.published_at = timezone.now()
            book.approved_by = request.user
            book.save()
        self.message_user(request, f'{queryset.count()} kitap yayınlandı.')
    publish_books.short_description = 'Seçili kitapları yayınla'
    
    def reject_books(self, request, queryset):
        updated = queryset.update(status='rejected')
        self.message_user(request, f'{updated} kitap reddedildi.')
    reject_books.short_description = 'Seçili kitapları reddet'
    
    def process_with_ai(self, request, queryset):
        # TODO: AI işleme fonksiyonunu çağır
        self.message_user(request, 'AI işleme başlatıldı (yakında eklenecek).')
    process_with_ai.short_description = 'AI ile işle (içindekiler + özet)'


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'book', 'order', 'level', 'page_start', 'page_end', 'word_count']
    list_filter = ['book', 'level', 'created_at']
    search_fields = ['title', 'book__title', 'content']
    readonly_fields = ['slug', 'created_at', 'updated_at']
    
    fieldsets = [
        ("Temel Bilgiler", {
            "fields": ['book', 'title', 'slug', 'order', 'level', 'parent']
        }),
        ("İçerik", {
            "fields": ['content', 'page_start', 'page_end', 'word_count']
        }),
        ("Tarihler", {
            "fields": ['created_at', 'updated_at'],
            "classes": ['collapse']
        }),
    ]


@admin.register(BookSummary)
class BookSummaryAdmin(admin.ModelAdmin):
    list_display = ['book', 'chapter', 'summary_type', 'generated_by', 'word_count', 'is_premium_only', 'generated_at']
    list_filter = ['summary_type', 'generated_by', 'is_premium_only', 'generated_at']
    search_fields = ['book__title', 'chapter__title', 'content']
    readonly_fields = ['generated_at', 'word_count', 'token_count']
    
    fieldsets = [
        ("Bağlantı", {
            "fields": ['book', 'chapter', 'summary_type']
        }),
        ("Özet", {
            "fields": ['content']
        }),
        ("AI Bilgileri", {
            "fields": ['generated_by', 'generated_at', 'token_count', 'word_count'],
            "classes": ['collapse']
        }),
        ("Erişim", {
            "fields": ['is_premium_only']
        }),
    ]

