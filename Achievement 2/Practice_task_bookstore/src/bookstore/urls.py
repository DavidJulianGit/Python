
from django.contrib import admin
from django.urls import path, include

# including media settings into urlpatterns
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.sales.urls')),
    path('books/', include('apps.books.urls') )
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)