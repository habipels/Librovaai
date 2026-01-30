from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SubscribedUsers
from django.utils.html import format_html


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_role_badge', 'is_premium_badge', 'is_author_approved', 'books_published', 'date_joined']
    list_filter = ['user_role', 'is_premium', 'is_author_approved', 'author_title', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Kullanıcı Rolü ve Yetkileri', {
            'fields': ('user_role', 'is_premium', 'premium_until')
        }),
        ('Yazar Bilgileri', {
            'fields': ('is_author_approved', 'author_title', 'author_bio', 'author_website'),
            'classes': ('collapse',)
        }),
        ('Profil', {
            'fields': ('image', 'description'),
            'classes': ('collapse',)
        }),
        ('İstatistikler', {
            'fields': ('books_published', 'total_readers'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_authors', 'make_premium', 'revoke_premium']
    
    def user_role_badge(self, obj):
        colors = {
            'reader': '#3498db',
            'author': '#e74c3c',
            'admin': '#2ecc71',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.user_role, 'gray'),
            obj.get_user_role_display()
        )
    user_role_badge.short_description = 'Rol'
    
    def is_premium_badge(self, obj):
        if obj.is_premium_active:
            return format_html('<span style="color: #f39c12; font-weight: bold;">⭐ Premium</span>')
        return format_html('<span style="color: gray;">Normal</span>')
    is_premium_badge.short_description = 'Üyelik'
    
    def approve_authors(self, request, queryset):
        updated = queryset.filter(user_role='author').update(is_author_approved=True)
        self.message_user(request, f'{updated} yazar onaylandı.')
    approve_authors.short_description = 'Seçili yazarları onayla'
    
    def make_premium(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        premium_until = timezone.now() + timedelta(days=365)
        updated = queryset.update(is_premium=True, premium_until=premium_until)
        self.message_user(request, f'{updated} kullanıcı premium yapıldı (1 yıl).')
    make_premium.short_description = 'Premium yap (1 yıl)'
    
    def revoke_premium(self, request, queryset):
        updated = queryset.update(is_premium=False, premium_until=None)
        self.message_user(request, f'{updated} kullanıcının premium üyeliği iptal edildi.')
    revoke_premium.short_description = 'Premium iptal et'


@admin.register(SubscribedUsers)
class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ['email_badge', 'name', 'created_badge', 'status_badge']
    search_fields = ['email', 'name']
    list_filter = ['created_date']
    readonly_fields = ['created_date']
    
    fieldsets = [
        ("Abone Bilgileri", {
            "fields": ['email', 'name']
        }),
        ("Tarih", {
            "fields": ['created_date']
        }),
    ]
    
    actions = ['export_emails']
    
    def email_badge(self, obj):
        return format_html(
            '<a href="mailto:{}" style="color: #667eea; text-decoration: none; font-weight: 500;">📧 {}</a>',
            obj.email,
            obj.email
        )
    email_badge.short_description = 'E-posta'
    
    def created_badge(self, obj):
        return format_html(
            '<span style="color: #6c757d; font-size: 12px;">🗓️ {}</span>',
            obj.created_date.strftime('%d.%m.%Y %H:%M')
        )
    created_badge.short_description = 'Kayıt Tarihi'
    
    def status_badge(self, obj):
        return format_html(
            '<span style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); color: white; padding: 3px 10px; border-radius: 12px; font-size: 11px;">✓ Aktif</span>'
        )
    status_badge.short_description = 'Durum'
    
    def export_emails(self, request, queryset):
        emails = [user.email for user in queryset]
        email_list = ', '.join(emails)
        self.message_user(request, f'E-postalar: {email_list}')
    export_emails.short_description = 'E-postaları listele'