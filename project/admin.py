# File: admin.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: December 2025
# Description: Django admin configuration for the guitar tabs application (tabby)

from django.contrib import admin
from .models import Song, Chord, Tab, UserFavorite, Exercise

# Register your models here.

admin.site.register(Song)
admin.site.register(Chord)
admin.site.register(Tab)
admin.site.register(UserFavorite)
admin.site.register(Exercise)
