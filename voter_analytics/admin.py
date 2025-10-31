# File: admin.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: October 2025
# Description: Admin configuration for voter_analytics app

from django.contrib import admin
from .models import Voter

# register the Voter model with the admin site
admin.site.register(Voter)