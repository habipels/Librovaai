"""
URL Configuration for Book Platform
"""

from django.urls import path
from . import book_views, admin_views

urlpatterns = [
    # ==================== GENEL SAYFALAR ====================
    path('', book_views.home, name='home'),
    path('books/', book_views.books_list, name='books_list'),
    path('book/<slug:slug>/', book_views.book_detail, name='book_detail'),
    path('book/<slug:slug>/read/', book_views.book_read, name='book_read'),
    path('book/<slug:slug>/chapter/<slug:chapter_slug>/', book_views.chapter_read, name='chapter_read'),
    
    path('categories/', book_views.categories_list, name='categories_list'),
    path('category/<slug:slug>/', book_views.category_detail, name='category_detail'),
    
    path('my-library/', book_views.my_library, name='my_library'),
    path('premium/', book_views.premium_upgrade, name='premium_upgrade'),
    path('contact/', book_views.contact, name='contact'),
    
    # AJAX endpoints
    path('book/<slug:slug>/bookmark/', book_views.add_bookmark, name='add_bookmark'),
    path('book/<slug:slug>/rate/', book_views.add_rating, name='add_rating'),
    
    # Yazar profili
    path('author/<str:username>/', book_views.author_profile, name='author_profile'),
    
    # ==================== YAZAR PANELİ ====================
    path('author/dashboard/', book_views.author_dashboard, name='author_dashboard'),
    path('author/my-books/', book_views.author_my_books, name='author_my_books'),
    path('author/upload-book/', book_views.author_upload_book, name='author_upload_book'),
    path('author/edit-book/<slug:slug>/', book_views.author_edit_book, name='author_edit_book'),
    path('author/pending/', book_views.author_pending, name='author_pending'),
    path('become-author/', book_views.become_author, name='become_author'),
    
    # ==================== ADMIN PANELİ ====================
    path('admin-panel/', admin_views.admin_dashboard, name='admin_dashboard'),
    
    # Kitap yönetimi
    path('admin-panel/books/', admin_views.admin_books, name='admin_books'),
    path('admin-panel/books/<int:pk>/', admin_views.admin_book_detail, name='admin_book_detail'),
    path('admin-panel/books/<int:pk>/delete/', admin_views.admin_book_delete, name='admin_book_delete'),
    
    # Yazar yönetimi
    path('admin-panel/authors/', admin_views.admin_authors, name='admin_authors'),
    path('admin-panel/authors/<int:pk>/', admin_views.admin_author_detail, name='admin_author_detail'),
    
    # Kullanıcı yönetimi
    path('admin-panel/users/', admin_views.admin_users, name='admin_users'),
    path('admin-panel/users/<int:pk>/', admin_views.admin_user_detail, name='admin_user_detail'),
    
    # Kategori yönetimi
    path('admin-panel/categories/', admin_views.admin_categories, name='admin_categories'),
    path('admin-panel/categories/<int:pk>/delete/', admin_views.admin_category_delete, name='admin_category_delete'),
    
    # Premium yönetimi
    path('admin-panel/premium/', admin_views.admin_premium, name='admin_premium'),
    
    # İstatistikler
    path('admin-panel/statistics/', admin_views.admin_statistics, name='admin_statistics'),
    
    # Site ayarları
    path('admin-panel/settings/', admin_views.admin_site_settings, name='admin_site_settings'),
]
