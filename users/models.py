from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import os

class CustomUser(AbstractUser):
    def image_upload_to(self, instance=None):
        if instance:
            return os.path.join("Users", self.username, instance)
        return None

    # Kullanıcı Rolleri
    ROLE_CHOICES = (
        ('reader', 'Okuyucu'),
        ('author', 'Yazar'),
        ('admin', 'Admin'),
    )
    
    # Kullanıcı Durumu
    STATUS = (
        ('regular', 'Normal'),
        ('premium', 'Premium'),
        ('moderator', 'Moderatör'),
    )
    
    # Yazar Ünvanları
    TITLE_CHOICES = (
        ('student', 'Öğrenci'),
        ('academician', 'Akademisyen'),
        ('researcher', 'Araştırmacı'),
        ('teacher', 'Öğretmen'),
        ('doctor', 'Doktor'),
        ('professor', 'Profesör'),
        ('writer', 'Yazar'),
        ('other', 'Diğer'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='reader')
    status = models.CharField(max_length=100, choices=STATUS, default='regular')
    description = models.TextField("Açıklama", max_length=600, default='', blank=True)
    image = models.ImageField(default='default/user.jpg', upload_to=image_upload_to)
    
    # Yazar Özel Alanları
    title = models.CharField("Ünvan", max_length=20, choices=TITLE_CHOICES, blank=True, null=True)
    is_author_approved = models.BooleanField("Yazar Onayı", default=False)
    author_bio = models.TextField("Yazar Biyografisi", max_length=1000, blank=True, default='')
    
    # Premium Üyelik
    is_premium = models.BooleanField("Premium Üye", default=False)
    premium_start_date = models.DateTimeField("Premium Başlangıç", blank=True, null=True)
    premium_end_date = models.DateTimeField("Premium Bitiş", blank=True, null=True)
    
    created_at = models.DateTimeField("Kayıt Tarihi", auto_now_add=True)
    updated_at = models.DateTimeField("Güncellenme", auto_now=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def is_author(self):
        return self.role == 'author' and self.is_author_approved
    
    def is_admin_user(self):
        return self.role == 'admin' or self.is_superuser
    
    def can_view_summaries(self):
        """Kullanıcı özet görebilir mi?"""
        return self.is_premium or self.status == 'premium'
    
    class Meta:
        verbose_name = "Kullanıcı"
        verbose_name_plural = "Kullanıcılar"
        ordering = ['-created_at']

class SubscribedUsers(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    created_date = models.DateTimeField('Date created', default=timezone.now)

    def __str__(self):
        return self.email