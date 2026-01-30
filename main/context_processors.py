from .models import SiteSettings


def site_settings(request):
    """
    Context processor - tüm template'lerde site_settings objesini kullanılabilir yapar
    
    Kullanım:
    {{ site_settings.site_name }}
    {{ site_settings.logo.url }}
    {{ site_settings.contact_email }}
    """
    settings = SiteSettings.get_settings()
    
    return {
        'site_settings': settings,
        'site_name': settings.site_name,
        'site_logo': settings.logo,
        'maintenance_mode': settings.maintenance_mode,
    }
