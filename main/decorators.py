"""
Kitap Platformu için Decorator'lar
Rol bazlı yetkilendirme ve premium kontrolleri
"""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def user_is_superuser(function=None, redirect_url='/'):
    """
    Decorator for views that checks that the user is superuser, redirecting
    to the homepage if necessary by default.
    """
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_superuser:
                messages.error(request, "You are not authorized to access this!")
                return redirect(redirect_url)
                
            return view_func(request, *args, **kwargs)

        return _wrapped_view

    if function:
        return decorator(function)

    return decorator


# ==================== YENİ DECORATORS ====================

def role_required(*roles):
    """
    Belirli rollere sahip kullanıcılar için decorator
    Kullanım: @role_required('author', 'admin')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role in roles or request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Bu sayfaya erişim yetkiniz yok.")
                raise PermissionDenied("Bu sayfaya erişim yetkiniz yok.")
        return _wrapped_view
    return decorator


def author_required(view_func):
    """
    Onaylı yazar için decorator
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_author() or request.user.is_admin_user():
            return view_func(request, *args, **kwargs)
        elif request.user.role == 'author' and not request.user.is_author_approved:
            messages.warning(request, "Yazar hesabınız henüz onaylanmamış. Admin onayını bekleyin.")
            return redirect('author_pending')
        else:
            messages.error(request, "Bu işlem için yazar olmalısınız.")
            return redirect('become_author')
    return _wrapped_view


def admin_required(view_func):
    """
    Admin için decorator
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_admin_user():
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "Bu sayfaya sadece adminler erişebilir.")
            raise PermissionDenied("Admin yetkisi gerekli.")
    return _wrapped_view


def premium_required(view_func):
    """
    Premium üye için decorator
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.can_view_summaries() or request.user.is_admin_user():
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, "Bu içerik sadece premium üyeler için. Üyeliğinizi yükseltin!")
            return redirect('premium_upgrade')
    return _wrapped_view


def ajax_premium_required(view_func):
    """
    AJAX istekleri için premium kontrolü
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if request.user.can_view_summaries() or request.user.is_admin_user():
            return view_func(request, *args, **kwargs)
        else:
            from django.http import JsonResponse
            return JsonResponse({
                'error': 'Premium üyelik gerekli',
                'premium_required': True
            }, status=403)
    return _wrapped_view


def book_owner_or_admin(view_func):
    """
    Kitap sahibi veya admin için decorator
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        from main.models import Book
        
        # URL'den book_id veya slug al
        book_id = kwargs.get('book_id') or kwargs.get('pk')
        book_slug = kwargs.get('slug')
        
        try:
            if book_id:
                book = Book.objects.get(id=book_id)
            elif book_slug:
                book = Book.objects.get(slug=book_slug)
            else:
                messages.error(request, "Kitap bulunamadı.")
                return redirect('books_list')
            
            # Kitap sahibi veya admin kontrolü
            if book.author == request.user or request.user.is_admin_user():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Bu kitap üzerinde yetkiniz yok.")
                raise PermissionDenied("Bu kitap üzerinde yetkiniz yok.")
                
        except Book.DoesNotExist:
            messages.error(request, "Kitap bulunamadı.")
            return redirect('books_list')
            
    return _wrapped_view


def check_book_access(view_func):
    """
    Kitaba erişim kontrolü
    - Yayında olan kitaplar herkese açık
    - Taslak/Bekleyen kitaplar sadece sahibi ve admin görebilir
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        from main.models import Book
        
        book_slug = kwargs.get('slug')
        
        try:
            book = Book.objects.get(slug=book_slug)
            
            # Yayında ise herkes görebilir
            if book.status == 'published':
                return view_func(request, *args, **kwargs)
            
            # Diğer durumlar için giriş gerekli
            if not request.user.is_authenticated:
                messages.warning(request, "Bu kitabı görüntülemek için giriş yapmalısınız.")
                return redirect('login')
            
            # Kitap sahibi veya admin görebilir
            if book.author == request.user or request.user.is_admin_user():
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "Bu kitap henüz yayında değil.")
                raise PermissionDenied("Kitap yayında değil.")
                
        except Book.DoesNotExist:
            messages.error(request, "Kitap bulunamadı.")
            return redirect('books_list')
            
    return _wrapped_view