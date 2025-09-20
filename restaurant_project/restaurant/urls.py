from django.urls import path
from . import views

# URL patterns for the restaurant app
urlpatterns = [
    path('main/', views.main, name='main'),
    path('order/', views.order, name='order'),
    path('confirmation/', views.confirmation, name='confirmation'),
]