from django.urls import path
from . import views
from django.conf import settings

app_name = 'mini_insta'

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.show_profile, name='show_profile'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('profile/<int:pk>/create_post/', views.CreatePostView.as_view(), name='create_post'),
]