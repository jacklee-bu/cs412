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

    def get_all_posts(self):
        # get all posts for this profile
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        return f"Post by {self.profile.username} at {self.timestamp}"

    def get_all_photos(self):
        # get all photos for this post
        photos = Photo.objects.filter(post=self).order_by('timestamp')
        return photos

class Photo(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for post {self.post.id}"
