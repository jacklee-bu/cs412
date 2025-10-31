# File: urls.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: October 2025
# Description: URL configuration for voter_analytics app

from django.urls import path
from .views import VoterListView, VoterDetailView, GraphsView

app_name = 'voter_analytics'

urlpatterns = [
    # main page showing all voters with filtering
    path('', VoterListView.as_view(), name='voters'),
    # detail page for a single voter
    path('voter/<int:pk>', VoterDetailView.as_view(), name='voter'),
    # graphs page
    path('graphs', GraphsView.as_view(), name='graphs'),
]