from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    login_view, logout_view, signup_view,
    serve_robots_txt, serve_security_txt, serve_google_verification
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.recipe.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', signup_view, name='signup'),
    # Security and SEO files - served directly
    path('robots.txt', serve_robots_txt, name='robots'),
    path('.well-known/security.txt', serve_security_txt, name='security'),
    # Google Search Console verification
    path('googlea962b821893d70d8.html', serve_google_verification, name='google-verification'),
]

# Serve media files in both development and production
# NOTE: For production, you should use cloud storage (AWS S3, Cloudinary)
# This is a temporary solution for Heroku
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

