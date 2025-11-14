# File: urls.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: November 2025
# Description: URL patterns for dadjokes app

from django.urls import path
from . import views
from . import api_views

app_name = 'dadjokes'

urlpatterns = [
    path('', views.random_view, name='random'),
    path('random/', views.random_view, name='random_page'),
    path('jokes/', views.jokes_view, name='jokes'),
    path('joke/<int:pk>/', views.joke_detail, name='joke_detail'),
    path('pictures/', views.pictures_view, name='pictures'),
    path('picture/<int:pk>/', views.picture_detail, name='picture_detail'),

    path('api/', api_views.api_random_joke, name='api_random'),
    path('api/random/', api_views.api_random_joke, name='api_random_joke'),
    path('api/jokes/', api_views.api_jokes, name='api_jokes'),
    path('api/joke/<int:pk>/', api_views.api_joke_detail, name='api_joke_detail'),
    path('api/pictures/', api_views.api_pictures, name='api_pictures'),
    path('api/picture/<int:pk>/', api_views.api_picture_detail, name='api_picture_detail'),
    path('api/random_picture/', api_views.api_random_picture, name='api_random_picture'),
]
