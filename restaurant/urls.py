# File: restaurant/urls.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: September 2024
# Description: URL patterns for the restaurant application

from django.urls import path
from . import views

# URL patterns for the restaurant app
urlpatterns = [
    path('', views.main, name='main'),
    path('main/', views.main, name='main_alt'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]