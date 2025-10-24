# Jack Lee
# jacklee@bu.edu
# urls.py for mini_insta app - defines URL routing patterns

from django.urls import path
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views

app_name = 'mini_insta'

urlpatterns = [
    path('', views.ProfileListView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.show_profile, name='show_profile'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='update_post'),
    # new URL patterns for A6
    path('profile/<int:pk>/followers/', views.ShowFollowersDetailView.as_view(), name='show_followers'),
    path('profile/<int:pk>/following/', views.ShowFollowingDetailView.as_view(), name='show_following'),
    # refactored URLs for A7 - no pk needed for authenticated user operations
    path('profile/', views.ShowOwnProfileView.as_view(), name='show_own_profile'),
    path('profile/feed/', views.PostFeedListView.as_view(), name='show_feed'),
    path('profile/search/', views.SearchView.as_view(), name='search'),
    path('profile/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('profile/create_post/', views.CreatePostView.as_view(), name='create_post'),
    # authentication URLs for A7
    path('login/', auth_views.LoginView.as_view(template_name='mini_insta/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='mini_insta:logout_confirmation'), name='logout'),
    path('logout_confirmation/', views.LogoutConfirmationView.as_view(), name='logout_confirmation'),
    # user registration for A7
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    # follow and like functionality for A7
    path('profile/<int:pk>/follow/', views.FollowProfileView.as_view(), name='follow'),
    path('profile/<int:pk>/delete_follow/', views.UnfollowProfileView.as_view(), name='delete_follow'),
    path('post/<int:pk>/like/', views.LikePostView.as_view(), name='like'),
    path('post/<int:pk>/delete_like/', views.UnlikePostView.as_view(), name='delete_like'),
]