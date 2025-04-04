
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('hidden_admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('resources/', include('apps.resources.urls')),
    path('', include('apps.home.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
   
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    