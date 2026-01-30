from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import os

class CustomUser(AbstractUser):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("Users", self.username, instance)
        return None

    USER_ROLE_CHOICES = (
        ('reader', 'Okuyucu'),
        ('author', 'Yazar'),
        ('admin', 'Admin'),
    )
    
    AUTHOR_TITLE_CHOICES = (
        ('student', 'Öğrenci'),
        ('academic', 'Akademisyen'),
        ('researcher', 'Araştırmacı'),
        ('writer', 'Yazar'),
        ('professor', 'Profesör'),
        ('doctor', 'Doktor'),
        ('other', 'Diğer'),
    )

    STATUS = (
        ('regular', 'regular'),
        ('subscriber', 'subscriber'),
        ('moderator', 'moderator'),
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField("Açıklama", max_length=600, default='', blank=True)
    image = models.ImageField("Profil Resmi", default='default/user.jpg', upload_to=image_upload_to)
    
    # Yeni alanlar
    user_role = models.CharField("Kullanıcı Rolü", max_length=20, choices=USER_ROLE_CHOICES, default='reader')
    is_premium = models.BooleanField("Premium Üye", default=False)
    premium_until = models.DateTimeField("Premium Bitiş Tarihi", null=True, blank=True)
    
    # Yazar özellikleri
    is_author_approved = models.BooleanField("Yazar Onayı", default=False, help_text="Admin tarafından onaylanmış yazar")
    author_title = models.CharField("Yazar Ünvanı", max_length=20, choices=AUTHOR_TITLE_CHOICES, default='writer', blank=True)
    author_bio = models.TextField("Yazar Biyografisi", max_length=2000, default='', blank=True)
    author_website = models.URLField("Website", max_length=200, blank=True)
    
    # İstatistikler
    books_published = models.IntegerField("Yayınlanan Kitap Sayısı", default=0)
    total_readers = models.IntegerField("Toplam Okuyucu Sayısı", default=0)

    def __str__(self):
        return self.username
    
    @property
    def is_premium_active(self):
        """Premium üyeliğin aktif olup olmadığını kontrol eder"""
        if not self.is_premium:
            return False
        if self.premium_until is None:
            return True  # Sınırsız premium
        return timezone.now() < self.premium_until
    
    @property
    def can_publish_books(self):
        """Kitap yayınlama yetkisi var mı?"""
        return self.user_role == 'author' and self.is_author_approved

    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"

class SubscribedUsers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.email