from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, SubscribedUsers


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'role', 'status', 'is_premium', 'is_author_approved', 'created_at']
    list_filter = ['role', 'status', 'is_premium', 'is_author_approved', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Rol ve Durum', {
            'fields': ('role', 'status', 'description')
        }),
        ('Yazar Bilgileri', {
            'fields': ('title', 'is_author_approved', 'author_bio'),
            'classes': ['collapse']
        }),
        ('Premium Bilgileri', {
            'fields': ('is_premium', 'premium_start_date', 'premium_end_date'),
            'classes': ['collapse']
        }),
        ('Profil', {
            'fields': ('image',),
            'classes': ['collapse']
        }),
    )


@admin.register(SubscribedUsers)
class SubscribedUsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'created_date')
    search_fields = ['email', 'name']
    list_filter = ['created_date']