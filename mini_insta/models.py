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

    def get_absolute_url(self):
        """Get the URL for this profile.
        Returns: URL string
        """
        from django.urls import reverse
        return reverse('mini_insta:show_profile',
                      kwargs={'pk': self.pk})

    def get_followers(self):
        """Get list of profiles who follow this profile.
        Returns: list of Profile objects
        """
        # get all Follow objects where this profile is being followed
        follow_objects = Follow.objects.filter(profile=self)
        # extract the follower profiles from the Follow objects
        followers = [follow.follower_profile for follow in follow_objects]
        return followers

    def get_num_followers(self):
        """Get count of followers.
        Returns: integer count
        """
        # count how many people follow this profile
        return Follow.objects.filter(profile=self).count()

    def get_following(self):
        """Get list of profiles this profile follows.
        Returns: list of Profile objects
        """
        # get all Follow objects where this profile is doing the following
        follow_objects = Follow.objects.filter(follower_profile=self)
        # extract the profiles being followed
        following = [follow.profile for follow in follow_objects]
        return following

    def get_num_following(self):
        """Get count of profiles being followed.
        Returns: integer count
        """
        # count how many profiles this one follows
        return Follow.objects.filter(follower_profile=self).count()

    def get_post_feed(self):
        """Get post feed for this profile.
        Returns: QuerySet of Post objects
        """
        # get profiles this user follows
        following_profiles = self.get_following()
        # get posts from those profiles, ordered by most recent
        posts = Post.objects.filter(profile__in=following_profiles).order_by('-timestamp')
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

    def get_absolute_url(self):
        """Get the URL for this post.
        Returns: URL string
        """
        from django.urls import reverse
        return reverse('mini_insta:post_detail',
                      kwargs={'pk': self.pk})

    def get_all_comments(self):
        """Get all comments for this post ordered by timestamp.
        Returns: QuerySet of Comment objects
        """
        # get all comments for this post
        comments = Comment.objects.filter(post=self).order_by('timestamp')
        return comments

    def get_likes(self):
        """Get all likes for this post.
        Returns: QuerySet of Like objects
        """
        # get all likes for this post
        likes = Like.objects.filter(post=self)
        return likes

class Photo(models.Model):
    """Model representing a photo attached to a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(max_length=500, blank=True)
    image_file = models.ImageField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the photo."""
        # check which type of photo this is
        if self.image_file:
            return f"Photo (file) for post {self.post.id}"
        else:
            return f"Photo (url) for post {self.post.id}"

    def get_image_url(self):
        """Get the URL for the image.
        Returns: URL string
        """
        # check if we have a URL first (backwards compatibility)
        if self.image_url:
            return self.image_url
        # otherwise use the uploaded file
        elif self.image_file:
            return self.image_file.url
        return ""

class Follow(models.Model):
    """Model representing a follow relationship between two profiles."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                               related_name="profile")
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE,
                                        related_name="follower_profile")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the follow relationship."""
        # show who follows who
        return f"{self.follower_profile.display_name} follows {self.profile.display_name}"

class Comment(models.Model):
    """Model representing a comment on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __str__(self):
        """Return string representation of the comment."""
        # show who commented on what
        return f"Comment by {self.profile.username} on post {self.post.id}"

class Like(models.Model):
    """Model representing a like on a post."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the like."""
        # show who liked what
        return f"{self.profile.display_name} liked post {self.post.id}"
