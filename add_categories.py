"""
Kitap kategorilerini veritabanına ekleyen script
"""
import os
import django

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djang_website.settings')
django.setup()

from main.models import BookCategory

# Kategoriler
categories = [
    {
        'name': 'Veri Bilimi',
        'description': 'Veri analizi, istatistik ve veri görselleştirme',
        'icon': 'fa-chart-bar',
        'color': '#3498db',
        'order': 1
    },
    {
        'name': 'Yapay Zeka',
        'description': 'AI, derin öğrenme ve sinir ağları',
        'icon': 'fa-brain',
        'color': '#9b59b6',
        'order': 2
    },
    {
        'name': 'Makine Öğrenmesi',
        'description': 'ML algoritmaları ve uygulamaları',
        'icon': 'fa-robot',
        'color': '#e74c3c',
        'order': 3
    },
    {
        'name': 'Web Geliştirme',
        'description': 'Frontend ve backend web teknolojileri',
        'icon': 'fa-code',
        'color': '#16a085',
        'order': 4
    },
    {
        'name': 'Mobil Uygulama',
        'description': 'iOS, Android ve cross-platform geliştirme',
        'icon': 'fa-mobile-alt',
        'color': '#f39c12',
        'order': 5
    },
    {
        'name': 'Veritabanı',
        'description': 'SQL, NoSQL ve veritabanı yönetimi',
        'icon': 'fa-database',
        'color': '#27ae60',
        'order': 6
    },
    {
        'name': 'Siber Güvenlik',
        'description': 'Güvenlik, şifreleme ve etik hacking',
        'icon': 'fa-shield-alt',
        'color': '#c0392b',
        'order': 7
    },
    {
        'name': 'Bulut Bilişim',
        'description': 'AWS, Azure, Google Cloud platformları',
        'icon': 'fa-cloud',
        'color': '#2980b9',
        'order': 8
    },
    {
        'name': 'Blockchain',
        'description': 'Kripto, akıllı sözleşmeler ve DeFi',
        'icon': 'fa-link',
        'color': '#f39c12',
        'order': 9
    },
    {
        'name': 'IoT',
        'description': 'Nesnelerin interneti ve gömülü sistemler',
        'icon': 'fa-microchip',
        'color': '#8e44ad',
        'order': 10
    },
    {
        'name': 'Oyun Geliştirme',
        'description': 'Unity, Unreal Engine ve oyun tasarımı',
        'icon': 'fa-gamepad',
        'color': '#e67e22',
        'order': 11
    },
    {
        'name': 'DevOps',
        'description': 'CI/CD, Docker, Kubernetes',
        'icon': 'fa-cogs',
        'color': '#34495e',
        'order': 12
    },
    {
        'name': 'Yazılım Mühendisliği',
        'description': 'Yazılım tasarımı ve mimari',
        'icon': 'fa-project-diagram',
        'color': '#16a085',
        'order': 13
    },
    {
        'name': 'İşletim Sistemleri',
        'description': 'Linux, Windows ve sistem yönetimi',
        'icon': 'fa-server',
        'color': '#2c3e50',
        'order': 14
    },
    {
        'name': 'Algoritma ve Veri Yapıları',
        'description': 'Programlama algoritmaları ve veri yapıları',
        'icon': 'fa-sitemap',
        'color': '#e74c3c',
        'order': 15
    },
    {
        'name': 'Bilgisayar Ağları',
        'description': 'Ağ protokolleri ve iletişim',
        'icon': 'fa-network-wired',
        'color': '#3498db',
        'order': 16
    },
    {
        'name': 'Grafik Tasarım',
        'description': 'Adobe Photoshop, Illustrator ve tasarım',
        'icon': 'fa-paint-brush',
        'color': '#e91e63',
        'order': 17
    },
    {
        'name': 'UI/UX Tasarım',
        'description': 'Kullanıcı deneyimi ve arayüz tasarımı',
        'icon': 'fa-palette',
        'color': '#9c27b0',
        'order': 18
    },
    {
        'name': 'Dijital Pazarlama',
        'description': 'SEO, sosyal medya ve içerik pazarlaması',
        'icon': 'fa-bullhorn',
        'color': '#ff9800',
        'order': 19
    },
    {
        'name': 'Proje Yönetimi',
        'description': 'Agile, Scrum ve proje planlama',
        'icon': 'fa-tasks',
        'color': '#607d8b',
        'order': 20
    },
]

# Kategorileri ekle
created_count = 0
updated_count = 0

for cat_data in categories:
    category, created = BookCategory.objects.update_or_create(
        name=cat_data['name'],
        defaults={
            'description': cat_data['description'],
            'icon': cat_data['icon'],
            'color': cat_data['color'],
            'order': cat_data['order'],
            'is_active': True
        }
    )
    
    if created:
        created_count += 1
        print(f"✅ Oluşturuldu: {category.name}")
    else:
        updated_count += 1
        print(f"🔄 Güncellendi: {category.name}")

print(f"\n{'='*50}")
print(f"Toplam: {len(categories)} kategori")
print(f"Yeni oluşturulan: {created_count}")
print(f"Güncellenen: {updated_count}")
print(f"{'='*50}")
