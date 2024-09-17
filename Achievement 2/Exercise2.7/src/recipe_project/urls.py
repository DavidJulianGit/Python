from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.recipes.views import home_view
from apps.auth.views import login_view, profile_view, logout_view, logout_success_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('', include('apps.recipes.urls')),
    path('markdownx/', include('markdownx.urls')),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
    path('logout-success/', logout_success_view, name='logout_success'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
