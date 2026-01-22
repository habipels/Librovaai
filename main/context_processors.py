"""
Context Processor - Site Ayarlarını Tüm Template'lere Ekle
"""

from .models import SiteSettings


def site_settings(request):
    """
    Site ayarlarını tüm template'lere ekler
    Kullanım: {{ site_settings.site_name }}
    """
    settings = SiteSettings.get_settings()
    
    return {
        'site_settings': settings,
        'site_name': settings.site_name,
        'site_logo': settings.site_logo,
        'maintenance_mode': settings.maintenance_mode,
    }
