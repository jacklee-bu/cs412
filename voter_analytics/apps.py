# File: apps.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: October 2025
# Description: App configuration for voter_analytics Django app

from django.apps import AppConfig


class VoterAnalyticsConfig(AppConfig):
    """Configuration class for the voter_analytics app."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'voter_analytics'