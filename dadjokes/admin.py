# File: admin.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: November 2025
# Description: Admin configuration for dadjokes app

from django.contrib import admin
from .models import Joke, Picture

admin.site.register(Joke)
admin.site.register(Picture)
