"""
Admin Panel Views
Admin tarafından kullanılan yönetim paneli
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib.auth import get_user_model

from .models import Book, Chapter, Category, BookRating
from .decorators import admin_required
from .ai_processor import process_book_file
from django.conf import settings

User = get_user_model()


@admin_required
def admin_dashboard(request):
    """Admin dashboard"""
    # İstatistikler
    total_books = Book.objects.count()
    total_users = User.objects.count()
    premium_users = User.objects.filter(is_premium=True).count()
    pending_books = Book.objects.filter(status='pending').count()
    
    # Onay bekleyen yazarlar
    pending_authors = User.objects.filter(role='author', is_author_approved=False).order_by('-created_at')[:5]
    
    # Onay bekleyen kitaplar
    pending_books_list = Book.objects.filter(status='pending').order_by('-created_at')[:5]
    
    # Son kitaplar
    recent_books = Book.objects.all().order_by('-created_at')[:10]
    
    context = {
        'total_books': total_books,
        'total_users': total_users,
        'premium_users': premium_users,
        'pending_books': pending_books,
        'pending_authors': pending_authors,
        'pending_books_list': pending_books_list,
        'recent_books': recent_books,
    }
    return render(request, 'admin_panel/dashboard.html', context)


@admin_required
def admin_books(request):
    """Kitap yönetimi"""
    books = Book.objects.all().order_by('-created_at')
    
    # Filtreleme
    status_filter = request.GET.get('status', '')
    if status_filter:
        books = books.filter(status=status_filter)
    
    search_query = request.GET.get('q', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Sayfalama
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)
    
    context = {
        'books': books_page,
        'status_filter': status_filter,
    }
    return render(request, 'admin_panel/books_list.html', context)


@admin_required
def admin_book_detail(request, pk):
    """Kitap detay ve onaylama"""
    book = get_object_or_404(Book, pk=pk)
    chapters = book.chapters.all().order_by('order', 'chapter_number')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            book.status = 'published'
            book.save()
            messages.success(request, f"'{book.title}' kitabı onaylandı ve yayınlandı.")
            
        elif action == 'reject':
            rejection_reason = request.POST.get('rejection_reason', '')
            book.status = 'rejected'
            book.rejection_reason = rejection_reason
            book.save()
            messages.warning(request, f"'{book.title}' kitabı reddedildi.")
            
        elif action == 'reprocess':
            # Kitabı yeniden işle
            try:
                result = process_book_file(
                    book_instance=book,
                    use_ai=getattr(settings, 'USE_AI_PROCESSING', False),
                    api_key=getattr(settings, 'OPENAI_API_KEY', None)
                )
                
                if result['success']:
                    messages.success(request, f"Kitap yeniden işlendi! {result['message']}")
                else:
                    messages.error(request, f"İşleme hatası: {result.get('error', 'Bilinmeyen hata')}")
            except Exception as e:
                messages.error(request, f"İşleme hatası: {str(e)}")
        
        return redirect('admin_book_detail', pk=book.pk)
    
    context = {
        'book': book,
        'chapters': chapters,
    }
    return render(request, 'admin_panel/book_detail.html', context)


@admin_required
def admin_book_delete(request, pk):
    """Kitap silme"""
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f"'{book_title}' kitabı silindi.")
        return redirect('admin_books')
    
    return render(request, 'admin_panel/book_delete_confirm.html', {'book': book})


@admin_required
def admin_authors(request):
    """Yazar yönetimi"""
    authors = User.objects.filter(role='author').order_by('-created_at')
    
    # Filtreleme
    approval_filter = request.GET.get('approval', '')
    if approval_filter == 'pending':
        authors = authors.filter(is_author_approved=False)
    elif approval_filter == 'approved':
        authors = authors.filter(is_author_approved=True)
    
    # Sayfalama
    paginator = Paginator(authors, 20)
    page_number = request.GET.get('page')
    authors_page = paginator.get_page(page_number)
    
    context = {
        'authors': authors_page,
        'approval_filter': approval_filter,
    }
    return render(request, 'admin_panel/authors_list.html', context)


@admin_required
def admin_author_detail(request, pk):
    """Yazar detay ve onaylama"""
    author = get_object_or_404(User, pk=pk, role='author')
    author_books = Book.objects.filter(author=author).order_by('-created_at')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            author.is_author_approved = True
            author.save()
            messages.success(request, f"{author.username} yazar olarak onaylandı.")
            
        elif action == 'reject':
            author.is_author_approved = False
            author.role = 'reader'
            author.save()
            messages.warning(request, f"{author.username} yazar başvurusu reddedildi.")
        
        return redirect('admin_author_detail', pk=author.pk)
    
    context = {
        'author': author,
        'author_books': author_books,
    }
    return render(request, 'admin_panel/author_detail.html', context)


@admin_required
def admin_users(request):
    """Kullanıcı yönetimi"""
    users = User.objects.all().order_by('-created_at')
    
    # Filtreleme
    role_filter = request.GET.get('role', '')
    if role_filter:
        users = users.filter(role=role_filter)
    
    search_query = request.GET.get('q', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Sayfalama
    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    
    context = {
        'users': users_page,
        'role_filter': role_filter,
    }
    return render(request, 'admin_panel/users_list.html', context)


@admin_required
def admin_user_detail(request, pk):
    """Kullanıcı detay"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'make_premium':
            user.is_premium = True
            user.status = 'premium'
            user.save()
            messages.success(request, f"{user.username} premium üye yapıldı.")
            
        elif action == 'remove_premium':
            user.is_premium = False
            user.status = 'regular'
            user.save()
            messages.success(request, f"{user.username} premium üyeliği kaldırıldı.")
            
        elif action == 'make_admin':
            user.role = 'admin'
            user.is_staff = True
            user.save()
            messages.success(request, f"{user.username} admin yapıldı.")
            
        elif action == 'ban':
            user.is_active = False
            user.save()
            messages.warning(request, f"{user.username} yasaklandı.")
            
        elif action == 'unban':
            user.is_active = True
            user.save()
            messages.success(request, f"{user.username} yasağı kaldırıldı.")
        
        return redirect('admin_user_detail', pk=user.pk)
    
    context = {'user_obj': user}
    return render(request, 'admin_panel/user_detail.html', context)


@admin_required
def admin_categories(request):
    """Kategori yönetimi"""
    categories = Category.objects.annotate(
        book_count=Count('books')
    ).order_by('name')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            
            if name:
                category, created = Category.objects.get_or_create(
                    name=name,
                    defaults={'description': description}
                )
                
                if created:
                    messages.success(request, f"'{name}' kategorisi oluşturuldu.")
                else:
                    messages.warning(request, "Bu kategori zaten mevcut.")
            
            return redirect('admin_categories')
    
    context = {'categories': categories}
    return render(request, 'admin_panel/categories.html', context)


@admin_required
def admin_category_delete(request, pk):
    """Kategori silme"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f"'{category_name}' kategorisi silindi.")
        return redirect('admin_categories')
    
    return render(request, 'admin_panel/category_delete_confirm.html', {'category': category})


@admin_required
def admin_premium(request):
    """Premium üyelik yönetimi"""
    premium_users = User.objects.filter(is_premium=True).order_by('-premium_start_date')
    
    # Sayfalama
    paginator = Paginator(premium_users, 20)
    page_number = request.GET.get('page')
    users_page = paginator.get_page(page_number)
    
    context = {'premium_users': users_page}
    return render(request, 'admin_panel/premium.html', context)


@admin_required
def admin_statistics(request):
    """İstatistikler"""
    from django.db.models import Sum
    
    # Genel istatistikler
    total_books = Book.objects.count()
    published_books = Book.objects.filter(status='published').count()
    total_users = User.objects.count()
    premium_users = User.objects.filter(is_premium=True).count()
    total_authors = User.objects.filter(role='author', is_author_approved=True).count()
    
    # Görüntülenme istatistikleri
    total_views = Book.objects.aggregate(total=Sum('view_count'))['total'] or 0
    
    # En çok görüntülenen kitaplar
    top_books = Book.objects.filter(status='published').order_by('-view_count')[:10]
    
    # En çok kitabı olan yazarlar
    top_authors = User.objects.filter(role='author').annotate(
        book_count=Count('books')
    ).order_by('-book_count')[:10]
    
    context = {
        'total_books': total_books,
        'published_books': published_books,
        'total_users': total_users,
        'premium_users': premium_users,
        'total_authors': total_authors,
        'total_views': total_views,
        'top_books': top_books,
        'top_authors': top_authors,
    }
    return render(request, 'admin_panel/statistics.html', context)


@admin_required
def admin_site_settings(request):
    """Site ayarları yönetimi"""
    from .models import SiteSettings
    
    settings_obj = SiteSettings.get_settings()
    
    if request.method == 'POST':
        # Temel bilgiler
        settings_obj.site_name = request.POST.get('site_name', settings_obj.site_name)
        settings_obj.site_description = request.POST.get('site_description', settings_obj.site_description)
        settings_obj.site_keywords = request.POST.get('site_keywords', settings_obj.site_keywords)
        
        # İletişim
        settings_obj.contact_email = request.POST.get('contact_email', settings_obj.contact_email)
        settings_obj.contact_phone = request.POST.get('contact_phone', settings_obj.contact_phone)
        settings_obj.contact_address = request.POST.get('contact_address', settings_obj.contact_address)
        
        # Sosyal medya
        settings_obj.facebook_url = request.POST.get('facebook_url', '')
        settings_obj.twitter_url = request.POST.get('twitter_url', '')
        settings_obj.instagram_url = request.POST.get('instagram_url', '')
        settings_obj.linkedin_url = request.POST.get('linkedin_url', '')
        settings_obj.youtube_url = request.POST.get('youtube_url', '')
        
        # Footer
        settings_obj.footer_text = request.POST.get('footer_text', settings_obj.footer_text)
        settings_obj.footer_about = request.POST.get('footer_about', settings_obj.footer_about)
        
        # SEO
        settings_obj.meta_title = request.POST.get('meta_title', settings_obj.meta_title)
        settings_obj.meta_description = request.POST.get('meta_description', settings_obj.meta_description)
        settings_obj.google_analytics_id = request.POST.get('google_analytics_id', '')
        settings_obj.google_site_verification = request.POST.get('google_site_verification', '')
        
        # Sistem ayarları
        settings_obj.maintenance_mode = request.POST.get('maintenance_mode') == 'on'
        settings_obj.maintenance_message = request.POST.get('maintenance_message', settings_obj.maintenance_message)
        settings_obj.default_language = request.POST.get('default_language', settings_obj.default_language)
        settings_obj.timezone = request.POST.get('timezone', settings_obj.timezone)
        
        # Özellik ayarları
        settings_obj.allow_registration = request.POST.get('allow_registration') == 'on'
        settings_obj.allow_comments = request.POST.get('allow_comments') == 'on'
        settings_obj.enable_ai_processing = request.POST.get('enable_ai_processing') == 'on'
        
        # Görseller
        site_logo = request.FILES.get('site_logo')
        if site_logo:
            settings_obj.site_logo = site_logo
        
        site_favicon = request.FILES.get('site_favicon')
        if site_favicon:
            settings_obj.site_favicon = site_favicon
        
        settings_obj.save()
        
        messages.success(request, "Site ayarları başarıyla güncellendi.")
        return redirect('admin_site_settings')
    
    context = {'settings': settings_obj}
    return render(request, 'admin_panel/site_settings.html', context)
