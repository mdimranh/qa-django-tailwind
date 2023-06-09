from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('home.urls')),
    path("auth/", include('user.urls')),
    path("", include('search.urls')),
    path("quran/", include('quran.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
