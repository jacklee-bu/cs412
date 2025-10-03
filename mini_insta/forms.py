from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption']  # dont include profile, will set it in the view