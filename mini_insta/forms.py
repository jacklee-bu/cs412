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