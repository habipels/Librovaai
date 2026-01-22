"""
Kitap Platformu - Views
Frontend görünümler (Okuyucu ve Yazar)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Book, Chapter, Category, BookRating, ReadingProgress, Bookmark
from .decorators import author_required, premium_required, book_owner_or_admin, check_book_access
from .ai_processor import process_book_file
from django.conf import settings


# ==================== GENEL SAYFA VIEW'LERI ====================

def home(request):
    """Ana sayfa"""
    featured_books = Book.objects.filter(status='published').order_by('-view_count')[:6]
    recent_books = Book.objects.filter(status='published').order_by('-published_at')[:8]
    categories = Category.objects.all()[:10]
    
    context = {
        'featured_books': featured_books,
        'recent_books': recent_books,
        'categories': categories,
    }
    return render(request, 'frontend/home.html', context)


def books_list(request):
    """Kitap listesi"""
    books = Book.objects.filter(status='published').order_by('-published_at')
    
    # Arama
    search_query = request.GET.get('q', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Kategori filtresi
    category_slug = request.GET.get('category', '')
    if category_slug:
        books = books.filter(categories__slug=category_slug)
    
    # Görünüm tipi
    view_type = request.GET.get('view', 'grid')
    
    # Sayfalama
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)
    
    # Kategoriler
    categories = Category.objects.all()
    
    context = {
        'books': books_page,
        'categories': categories,
        'view_type': view_type,
    }
    return render(request, 'frontend/books/books_list.html', context)


def book_detail(request, slug):
    """Kitap detay sayfası"""
    book = get_object_or_404(Book, slug=slug)
    
    # Görüntülenme sayısını artır
    book.view_count += 1
    book.save(update_fields=['view_count'])
    
    # Bölümler
    chapters = book.chapters.all().order_by('order', 'chapter_number')
    
    # Değerlendirmeler
    ratings = book.ratings.all().order_by('-created_at')[:10]
    
    # Kullanıcının okuma ilerlemesi
    reading_progress = None
    is_bookmarked = False
    
    if request.user.is_authenticated:
        reading_progress = ReadingProgress.objects.filter(
            user=request.user, 
            book=book
        ).first()
        
        is_bookmarked = Bookmark.objects.filter(
            user=request.user, 
            book=book
        ).exists()
    
    context = {
        'book': book,
        'chapters': chapters,
        'ratings': ratings,
        'reading_progress': reading_progress,
        'is_bookmarked': is_bookmarked,
    }
    return render(request, 'frontend/books/book_detail.html', context)


@login_required
@check_book_access
def book_read(request, slug):
    """Kitap okuma sayfası"""
    book = get_object_or_404(Book, slug=slug)
    
    # İlk bölümü al
    first_chapter = book.chapters.order_by('order', 'chapter_number').first()
    
    if first_chapter:
        return redirect('chapter_read', slug=book.slug, chapter_slug=first_chapter.slug)
    else:
        messages.warning(request, "Bu kitabın henüz bölümleri yüklenmemiş.")
        return redirect('book_detail', slug=book.slug)


@login_required
@check_book_access
def chapter_read(request, slug, chapter_slug):
    """Bölüm okuma"""
    book = get_object_or_404(Book, slug=slug)
    chapter = get_object_or_404(Chapter, book=book, slug=chapter_slug)
    
    # Tüm bölümler (navigasyon için)
    all_chapters = book.chapters.order_by('order', 'chapter_number')
    
    # Önceki ve sonraki bölüm
    prev_chapter = all_chapters.filter(order__lt=chapter.order).last()
    next_chapter = all_chapters.filter(order__gt=chapter.order).first()
    
    # Okuma ilerlemesini güncelle
    reading_progress, created = ReadingProgress.objects.get_or_create(
        user=request.user,
        book=book
    )
    reading_progress.chapter = chapter
    
    # İlerleme yüzdesini hesapla
    total_chapters = all_chapters.count()
    current_position = list(all_chapters).index(chapter) + 1
    reading_progress.progress_percentage = int((current_position / total_chapters) * 100)
    reading_progress.save()
    
    context = {
        'book': book,
        'chapter': chapter,
        'all_chapters': all_chapters,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
    }
    return render(request, 'frontend/books/chapter_read.html', context)


def categories_list(request):
    """Kategori listesi"""
    categories = Category.objects.annotate(
        book_count=Count('books', filter=Q(books__status='published'))
    ).order_by('name')
    
    context = {'categories': categories}
    return render(request, 'frontend/books/categories_list.html', context)


def category_detail(request, slug):
    """Kategori detay"""
    category = get_object_or_404(Category, slug=slug)
    books = Book.objects.filter(categories=category, status='published').order_by('-published_at')
    
    # Sayfalama
    paginator = Paginator(books, 12)
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'books': books_page,
    }
    return render(request, 'frontend/books/category_detail.html', context)


@login_required
def my_library(request):
    """Kullanıcının kütüphanesi"""
    # Başladığı kitaplar
    reading_books = ReadingProgress.objects.filter(user=request.user).order_by('-last_read_at')
    
    # Yer imleri
    bookmarks = Bookmark.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    # Değerlendirdiği kitaplar
    rated_books = BookRating.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    context = {
        'reading_books': reading_books,
        'bookmarks': bookmarks,
        'rated_books': rated_books,
    }
    return render(request, 'frontend/books/my_library.html', context)


@login_required
@require_POST
def add_bookmark(request, slug):
    """Yer imi ekle"""
    book = get_object_or_404(Book, slug=slug)
    
    # Kullanıcının en son okuduğu bölümü al
    progress = ReadingProgress.objects.filter(user=request.user, book=book).first()
    
    chapter = progress.chapter if progress else book.chapters.first()
    
    bookmark, created = Bookmark.objects.get_or_create(
        user=request.user,
        book=book,
        defaults={'chapter': chapter}
    )
    
    return JsonResponse({'success': True, 'created': created})


@login_required
@require_POST
def add_rating(request, slug):
    """Değerlendirme ekle"""
    book = get_object_or_404(Book, slug=slug)
    
    rating_value = request.POST.get('rating')
    review_text = request.POST.get('review', '')
    
    if not rating_value:
        messages.error(request, "Puan seçmelisiniz.")
        return redirect('book_detail', slug=slug)
    
    rating, created = BookRating.objects.update_or_create(
        user=request.user,
        book=book,
        defaults={
            'rating': int(rating_value),
            'review': review_text
        }
    )
    
    if created:
        messages.success(request, "Değerlendirmeniz kaydedildi.")
    else:
        messages.success(request, "Değerlendirmeniz güncellendi.")
    
    return redirect('book_detail', slug=slug)


def author_profile(request, username):
    """Yazar profil sayfası"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    author = get_object_or_404(User, username=username, role='author')
    
    # Yazar kitapları
    books = Book.objects.filter(author=author, status='published').order_by('-published_at')
    
    context = {
        'author': author,
        'books': books,
    }
    return render(request, 'frontend/author/author_profile.html', context)


def premium_upgrade(request):
    """Premium üyelik sayfası"""
    return render(request, 'frontend/premium_upgrade.html')


def contact(request):
    """İletişim sayfası"""
    return render(request, 'frontend/contact.html')


# ==================== YAZAR VIEW'LERI ====================

@author_required
def author_dashboard(request):
    """Yazar paneli"""
    my_books = Book.objects.filter(author=request.user).order_by('-created_at')
    
    # İstatistikler
    my_books_count = my_books.count()
    published_books_count = my_books.filter(status='published').count()
    pending_books_count = my_books.filter(status='pending').count()
    total_views = sum([book.view_count for book in my_books])
    
    context = {
        'my_books': my_books[:10],
        'my_books_count': my_books_count,
        'published_books_count': published_books_count,
        'pending_books_count': pending_books_count,
        'total_views': total_views,
    }
    return render(request, 'frontend/author/dashboard.html', context)


@author_required
def author_my_books(request):
    """Yazarın kitapları"""
    books = Book.objects.filter(author=request.user).order_by('-created_at')
    
    # Sayfalama
    paginator = Paginator(books, 20)
    page_number = request.GET.get('page')
    books_page = paginator.get_page(page_number)
    
    context = {'books': books_page}
    return render(request, 'frontend/author/my_books.html', context)


@author_required
def author_upload_book(request):
    """Kitap yükleme"""
    if request.method == 'POST':
        # Form verileri
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle', '')
        description = request.POST.get('description', '')
        publisher = request.POST.get('publisher', '')
        isbn = request.POST.get('isbn', '')
        publication_year = request.POST.get('publication_year')
        page_count = request.POST.get('page_count')
        language = request.POST.get('language', 'Türkçe')
        status = request.POST.get('status', 'pending')
        
        # Dosyalar
        book_file = request.FILES.get('file')
        cover_image = request.FILES.get('cover_image')
        
        # Kategoriler
        category_ids = request.POST.getlist('categories')
        
        # AI işleme
        process_with_ai = request.POST.get('process_with_ai') == '1'
        
        if not title or not book_file:
            messages.error(request, "Başlık ve dosya zorunludur.")
            return redirect('author_upload_book')
        
        # Kitap oluştur
        book = Book.objects.create(
            title=title,
            subtitle=subtitle,
            description=description,
            author=request.user,
            file=book_file,
            file_type=book_file.name.split('.')[-1].lower(),
            publisher=publisher,
            isbn=isbn,
            publication_year=publication_year if publication_year else None,
            page_count=page_count if page_count else None,
            language=language,
            status=status
        )
        
        # Kapak görseli
        if cover_image:
            book.cover_image = cover_image
            book.save()
        
        # Kategoriler
        if category_ids:
            book.categories.set(category_ids)
        
        # AI ile işle
        if process_with_ai:
            try:
                result = process_book_file(
                    book_instance=book,
                    use_ai=getattr(settings, 'USE_AI_PROCESSING', False),
                    api_key=getattr(settings, 'OPENAI_API_KEY', None)
                )
                
                if result['success']:
                    messages.success(request, f"Kitap başarıyla yüklendi ve işlendi! {result['message']}")
                else:
                    messages.warning(request, f"Kitap yüklendi ancak işleme hatası: {result.get('error', 'Bilinmeyen hata')}")
            except Exception as e:
                messages.warning(request, f"Kitap yüklendi ancak AI işleme hatası: {str(e)}")
        else:
            messages.success(request, "Kitap başarıyla yüklendi!")
        
        return redirect('author_dashboard')
    
    # GET
    categories = Category.objects.all().order_by('name')
    context = {'categories': categories}
    return render(request, 'frontend/author/upload_book.html', context)


@book_owner_or_admin
def author_edit_book(request, slug):
    """Kitap düzenleme"""
    book = get_object_or_404(Book, slug=slug)
    
    if request.method == 'POST':
        # Güncelleme işlemleri
        book.title = request.POST.get('title', book.title)
        book.subtitle = request.POST.get('subtitle', book.subtitle)
        book.description = request.POST.get('description', book.description)
        book.publisher = request.POST.get('publisher', book.publisher)
        book.isbn = request.POST.get('isbn', book.isbn)
        
        publication_year = request.POST.get('publication_year')
        if publication_year:
            book.publication_year = publication_year
        
        page_count = request.POST.get('page_count')
        if page_count:
            book.page_count = page_count
        
        book.language = request.POST.get('language', book.language)
        
        # Kapak görseli
        cover_image = request.FILES.get('cover_image')
        if cover_image:
            book.cover_image = cover_image
        
        # Kategoriler
        category_ids = request.POST.getlist('categories')
        if category_ids:
            book.categories.set(category_ids)
        
        book.save()
        
        messages.success(request, "Kitap başarıyla güncellendi.")
        return redirect('author_dashboard')
    
    # GET
    categories = Category.objects.all().order_by('name')
    context = {
        'book': book,
        'categories': categories,
    }
    return render(request, 'frontend/author/edit_book.html', context)


def author_pending(request):
    """Yazar onay bekleme sayfası"""
    return render(request, 'frontend/author/pending.html')


def become_author(request):
    """Yazar başvuru sayfası"""
    if request.method == 'POST':
        title = request.POST.get('title')
        bio = request.POST.get('bio', '')
        
        if not title:
            messages.error(request, "Ünvan seçmelisiniz.")
            return redirect('become_author')
        
        # Kullanıcıyı yazar yap
        request.user.role = 'author'
        request.user.title = title
        request.user.author_bio = bio
        request.user.is_author_approved = False
        request.user.save()
        
        messages.success(request, "Yazar başvurunuz alındı. Admin onayını bekleyin.")
        return redirect('author_pending')
    
    return render(request, 'frontend/author/become_author.html')
