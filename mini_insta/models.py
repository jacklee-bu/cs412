from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Profile(models.Model):
    bio_text = models.TextField(blank=True)
    username = models.CharField(max_length=100, unique=True)
    profile_image_url = models.URLField(max_length=500)
    display_name = models.CharField(max_length=100)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
