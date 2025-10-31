# File: cs412/urls.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: September 2024
# Description: Main URL configuration for CS412 restaurant project

"""
URL configuration for cs412 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quotes/', include('quotes.urls')),
    path('restaurant/', include('restaurant.urls')),
    path('mini_insta/', include('mini_insta.urls')),
    path('voter_analytics/', include('voter_analytics.urls')),
    # Also handle cs412/ prefix if Apache doesn't strip it
    path('cs412/quotes/', include('quotes.urls')),
    path('cs412/restaurant/', include('restaurant.urls')),
    path('cs412/mini_insta/', include('mini_insta.urls')),
    path('cs412/voter_analytics/', include('voter_analytics.urls')),
]

# serve media files during development only
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
