"""
Maintenance Mode Middleware
Bakım modu aktifken siteyi kapatır
"""

from django.shortcuts import render
from django.conf import settings
from .models import SiteSettings


class MaintenanceModeMiddleware:
    """
    Bakım modu aktifken normal kullanıcıları bakım sayfasına yönlendirir
    Admin ve staff kullanıcılar etkilenmez
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Ayarları kontrol et
        try:
            site_settings = SiteSettings.get_settings()
            
            # Bakım modu aktif mi?
            if site_settings.maintenance_mode:
                # Admin veya staff kullanıcı değilse
                if not request.user.is_authenticated or not (request.user.is_staff or request.user.is_superuser):
                    # Bazı URL'lere izin ver (admin, login, vb.)
                    allowed_paths = [
                        '/admin/',
                        '/login/',
                        '/logout/',
                    ]
                    
                    # Eğer izin verilen path'lerden biri değilse
                    if not any(request.path.startswith(path) for path in allowed_paths):
                        # Bakım sayfasını göster
                        return render(request, 'maintenance.html', {
                            'site_settings': site_settings,
                            'maintenance_message': site_settings.maintenance_message
                        }, status=503)
        
        except Exception:
            # Hata durumunda normal devam et
            pass
        
        response = self.get_response(request)
        return response
