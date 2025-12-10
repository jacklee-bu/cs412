# File: forms.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: December 2025
# Description: Form classes for creating and editing records in the
#              guitar tabs application (tabby).

from django import forms
from .models import Song, Chord, Tab, UserFavorite


class SongForm(forms.ModelForm):
    """Form for creating and editing songs."""
    class Meta:
        model = Song
        fields = ['title', 'artist', 'album', 'year']


class ChordForm(forms.ModelForm):
    """Form for creating and editing chords."""
    class Meta:
        model = Chord
        fields = ['name', 'full_name', 'fingering', 'difficulty', 'category']


class TabForm(forms.ModelForm):
    """Form for creating and editing guitar tabs."""
    class Meta:
        model = Tab
        fields = ['song', 'difficulty', 'content', 'chords_used', 'tuning', 'capo']


class UserFavoriteForm(forms.ModelForm):
    """Form for saving tabs to favorites and updating practice notes."""
    class Meta:
        model = UserFavorite
        fields = ['tab', 'notes', 'is_mastered']
