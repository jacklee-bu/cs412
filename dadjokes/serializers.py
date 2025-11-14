# File: serializers.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: November 2025
# Description: Serializers for dadjokes REST API

from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Joke
        fields = ['id', 'text', 'name', 'timestamp']


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'name', 'timestamp']
