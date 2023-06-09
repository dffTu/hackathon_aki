from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('client/', include('clients.urls')),
    path('catalogue/', include('platforms.urls')),
    path('catalogue_unverified/', include('administration.urls')),
    path('organizer/', include('organizers.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
