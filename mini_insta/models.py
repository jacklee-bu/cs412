# Jack Lee
# jacklee@bu.edu
# models.py for mini_insta app - defines Profile, Post, and Photo models

from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.

class Profile(models.Model):
    """Model representing a user profile in mini_insta."""
    bio_text = models.TextField(blank=True)
    username = models.CharField(max_length=100, unique=True)
    profile_image_url = models.URLField(max_length=500)
    display_name = models.CharField(max_length=100)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the profile."""
        return self.username

    def get_all_posts(self):
        """Get all posts for this profile ordered by timestamp.
        Returns: QuerySet of Post objects
        """
        # get all posts for this profile
        posts = Post.objects.filter(profile=self).order_by('-timestamp')
        return posts

class Post(models.Model):
    """Model representing a post by a profile."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)

    def __str__(self):
        """Return string representation of the post."""
        return f"Post by {self.profile.username} at {self.timestamp}"

    def get_all_photos(self):
        """Get all photos for this post ordered by timestamp.
        Returns: QuerySet of Photo objects
        """
        # get all photos for this post
        photos = Photo.objects.filter(post=self).order_by('timestamp')
        return photos

class Photo(models.Model):
    """Model representing a photo attached to a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the photo."""
        return f"Photo for post {self.post.id}"
