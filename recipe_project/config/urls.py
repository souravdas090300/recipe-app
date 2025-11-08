from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from .views import login_view, logout_view, signup_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.recipe.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    # Security and SEO files
    path('robots.txt', RedirectView.as_view(url=settings.STATIC_URL + 'robots.txt', permanent=True)),
    path('.well-known/security.txt', RedirectView.as_view(url=settings.STATIC_URL + '.well-known/security.txt', permanent=True)),
]

# Serve media files in both development and production
# NOTE: For production, you should use cloud storage (AWS S3, Cloudinary)
# This is a temporary solution for Heroku
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

