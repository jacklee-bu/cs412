# File: serializers.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: December 2025
# Description: Serializers for the guitar tabs REST API.
#              Converts model instances to JSON for the mobile app.

from rest_framework import serializers
from .models import Song, Chord, Tab, UserFavorite


class SongSerializer(serializers.ModelSerializer):
    """Serializer for the Song model."""
    class Meta:
        model = Song
        fields = ['id', 'title', 'artist', 'album', 'year']


class ChordSerializer(serializers.ModelSerializer):
    """Serializer for the Chord model."""
    class Meta:
        model = Chord
        fields = ['id', 'name', 'full_name', 'fingering', 'difficulty', 'category']


class TabSerializer(serializers.ModelSerializer):
    """Serializer for the Tab model."""
    class Meta:
        model = Tab
        fields = ['id', 'song', 'difficulty', 'content', 'chords_used', 'tuning', 'capo']


class UserFavoriteSerializer(serializers.ModelSerializer):
    """Serializer for the UserFavorite model."""
    class Meta:
        model = UserFavorite
        fields = ['id', 'tab', 'date_saved', 'practice_time', 'notes', 'is_mastered']
