# File: api_views.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: November 2025
# Description: API views for dadjokes REST API

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Joke, Picture
from .serializers import JokeSerializer, PictureSerializer
import random

@api_view(['GET'])
def api_random_joke(request):
    jokes = Joke.objects.all()

    if jokes:
        joke = random.choice(jokes)
        serializer = JokeSerializer(joke)
        return Response(serializer.data)
    else:
        return Response({'error': 'No jokes available'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
def api_jokes(request):
    if request.method == 'GET':
        jokes = Joke.objects.all()
        serializer = JokeSerializer(jokes, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JokeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def api_joke_detail(request, pk):
    try:
        joke = Joke.objects.get(pk=pk)
    except Joke.DoesNotExist:
        return Response({'error': 'Joke not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = JokeSerializer(joke)
    return Response(serializer.data)


@api_view(['GET'])
def api_pictures(request):
    pictures = Picture.objects.all()
    serializer = PictureSerializer(pictures, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_picture_detail(request, pk):
    try:
        picture = Picture.objects.get(pk=pk)
    except Picture.DoesNotExist:
        return Response({'error': 'Picture not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = PictureSerializer(picture)
    return Response(serializer.data)


@api_view(['GET'])
def api_random_picture(request):
    pictures = Picture.objects.all()

    if pictures:
        picture = random.choice(pictures)
        serializer = PictureSerializer(picture)
        return Response(serializer.data)
    else:
        return Response({'error': 'No pictures available'}, status=status.HTTP_404_NOT_FOUND)
