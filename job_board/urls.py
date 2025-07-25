"""
URL configuration for job_board project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView
from django.conf import settings # Import settings
from django.conf.urls.static import static # Import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('conturi/', include('accounts.urls')), # Include accounts app URLs
    path('locuri-de-munca/', include('jobs.urls')),         # Include jobs app URLs
    path('plati/', include('payments.urls')), # Include payments app URLs
        path('', include('core.urls')),              # Include core app URLs (homepage, etc.)
    path('ads.txt', RedirectView.as_view(url='/static/ads.txt')),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
