# Jack Lee
# jacklee@bu.edu
# forms.py for mini_insta app - defines forms for creating posts

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """Form for creating a new post with caption."""
    class Meta:
        model = Post
        fields = ['caption']  # dont include profile, will set it in the view

class UpdateProfileForm(forms.ModelForm):
    """Form for updating an existing profile."""
    class Meta:
        model = Profile
        # dont include username or join_date - those shouldnt change
        fields = ['bio_text', 'profile_image_url', 'display_name']

class UpdatePostForm(forms.ModelForm):
    """Form for updating an existing post."""
    class Meta:
        model = Post
        fields = ['caption']

class CreateProfileForm(forms.ModelForm):
    """Form for creating a new profile."""
    class Meta:
        model = Profile
        # exclude user and join_date - user will be set from UserCreationForm
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']