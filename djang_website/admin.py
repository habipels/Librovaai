from django.contrib import admin


# Monkey patch admin index view to add context
_original_index = admin.site.index

def custom_index(request, extra_context=None):
    from main.models import Book, Article
    from users.models import CustomUser
    
    extra_context = extra_context or {}
    extra_context['total_books'] = Book.objects.count()
    extra_context['total_users'] = CustomUser.objects.count()
    extra_context['total_articles'] = Article.objects.count()
    extra_context['pending_books'] = Book.objects.filter(status='pending').count()
    extra_context['recent_books'] = Book.objects.order_by('-created_at')[:5]
    extra_context['recent_users'] = CustomUser.objects.order_by('-date_joined')[:5]
    
    return _original_index(request, extra_context)

admin.site.index = custom_index
