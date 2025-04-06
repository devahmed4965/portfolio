# main project urls.py (e.g., portfolio_project/urls.py)

from django.contrib import admin
from django.urls import path, include # Make sure include is imported
from django.conf import settings # Optional: for media/static files in development
from django.conf.urls.static import static # Optional: for media/static files in development

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('portfolio.urls')), # Your app's URLs
    path('i18n/', include('django.conf.urls.i18n')), # <-- Add this line for language switching
]

# Optional: Add static and media serving for development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)