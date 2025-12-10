# File: urls.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: December 2025
# Description: URL routing for the guitar tabs application (tabby)

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from . import api_views

app_name = 'project'

urlpatterns = [
    # auth views
    path('login/', auth_views.LoginView.as_view(template_name='project/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),

    # web views
    path('', views.HomeView.as_view(), name='home'),
    path('tuner/', views.TunerView.as_view(), name='tuner'),
    path('exercises/', views.ExerciseListView.as_view(), name='exercise_list'),
    path('exercise/<int:pk>/', views.ExerciseDetailView.as_view(), name='exercise_detail'),
    path('exercise/new/', views.ExerciseCreateView.as_view(), name='exercise_create'),
    path('exercise/<int:pk>/edit/', views.ExerciseUpdateView.as_view(), name='exercise_update'),
    path('exercise/<int:pk>/delete/', views.ExerciseDeleteView.as_view(), name='exercise_delete'),
    path('songs/', views.SongListView.as_view(), name='song_list'),
    path('song/<int:pk>/', views.SongDetailView.as_view(), name='song_detail'),
    path('song/new/', views.SongCreateView.as_view(), name='song_create'),
    path('song/<int:pk>/edit/', views.SongUpdateView.as_view(), name='song_update'),
    path('song/<int:pk>/delete/', views.SongDeleteView.as_view(), name='song_delete'),

    path('chords/', views.ChordListView.as_view(), name='chord_list'),
    path('chord/<int:pk>/', views.ChordDetailView.as_view(), name='chord_detail'),
    path('chord/new/', views.ChordCreateView.as_view(), name='chord_create'),
    path('chord/<int:pk>/edit/', views.ChordUpdateView.as_view(), name='chord_update'),
    path('chord/<int:pk>/delete/', views.ChordDeleteView.as_view(), name='chord_delete'),

    path('tabs/', views.TabListView.as_view(), name='tab_list'),
    path('tab/<int:pk>/', views.TabDetailView.as_view(), name='tab_detail'),
    path('tab/new/', views.TabCreateView.as_view(), name='tab_create'),
    path('tab/<int:pk>/edit/', views.TabUpdateView.as_view(), name='tab_update'),
    path('tab/<int:pk>/delete/', views.TabDeleteView.as_view(), name='tab_delete'),

    path('favorites/', views.FavoriteListView.as_view(), name='favorite_list'),
    path('favorite/add/', views.FavoriteCreateView.as_view(), name='favorite_create'),
    path('favorite/<int:pk>/edit/', views.FavoriteUpdateView.as_view(), name='favorite_update'),
    path('favorite/<int:pk>/delete/', views.FavoriteDeleteView.as_view(), name='favorite_delete'),

    # API endpoints for mobile app
    path('api/songs/', api_views.api_songs, name='api_songs'),
    path('api/song/<int:pk>/', api_views.api_song_detail, name='api_song_detail'),
    path('api/chords/', api_views.api_chords, name='api_chords'),
    path('api/chord/<int:pk>/', api_views.api_chord_detail, name='api_chord_detail'),
    path('api/tabs/', api_views.api_tabs, name='api_tabs'),
    path('api/tab/<int:pk>/', api_views.api_tab_detail, name='api_tab_detail'),
    path('api/featured/', api_views.api_featured, name='api_featured'),
    path('api/search/', api_views.api_search, name='api_search'),
]
