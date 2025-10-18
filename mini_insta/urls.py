# Jack Lee
# jacklee@bu.edu
# urls.py for mini_insta app - defines URL routing patterns

from django.urls import path
from . import views
from django.conf import settings

app_name = 'mini_insta'

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.show_profile, name='show_profile'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('profile/<int:pk>/create_post/', views.CreatePostView.as_view(), name='create_post'),
    path('profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='update_post'),
    # new URL patterns for A6
    path('profile/<int:pk>/followers/', views.ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following/', views.ShowFollowingDetailView.as_view(), name='show_following'),
    path('profile/<int:pk>/feed/', views.PostFeedListView.as_view(), name='show_feed'),
    path('profile/<int:pk>/search/', views.SearchView.as_view(), name='search'),
]