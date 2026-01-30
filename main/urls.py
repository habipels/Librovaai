from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    
    # Blog URLs - SPESİFİK OLANLAR ÖNCE!
    path("blog/", views.blog_list, name="blog_list"),
    path("blog/<slug:series_slug>/", views.blog_series, name="blog_series"),
    path("blog/<slug:series_slug>/<slug:article_slug>/", views.blog_detail, name="blog_detail"),
    
    # Book URLs
    path("books/", views.book_list, name="book_list"),
    path("books/<slug:slug>/", views.book_detail, name="book_detail"),
    
    # Admin/Newsletter URLs
    path("newsletter/", views.newsletter, name="newsletter"),
    path("new_series/", views.new_series, name="series-create"),
    path("new_post/", views.new_post, name="post-create"),
    
    # Article/Series Management (CATCH-ALL PATTERNS EN SONDA!)
    path("<series>/", views.series, name="series"),
    path("<series>/update/", views.series_update, name="series_update"),
    path("<series>/delete/", views.series_delete, name="series_delete"),
    path("<series>/<article>/", views.article, name="article"),
    path("<series>/<article>/update/", views.article_update, name="article_update"),
    path("<series>/<article>/delete/", views.article_delete, name="article_delete"),
    path("<series>/<article>/upload_image/", views.upload_image, name="upload_image"),
]