# File: api_views.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: December 2025
# Description: REST API endpoints for the guitar tabs application.
#              Provides JSON data for the React Native mobile app.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Song, Chord, Tab
from .serializers import SongSerializer, ChordSerializer, TabSerializer


@api_view(['GET'])
def api_songs(request):
    """Return all songs, optionally filtered by search query.

    GET parameters:
        q: search string to filter by title or artist
    """
    query = request.GET.get('q', '')
    if query:
        songs = Song.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query))
    else:
        songs = Song.objects.all()
    serializer = SongSerializer(songs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_song_detail(request, pk):
    """Return a single song by its ID."""
    try:
        song = Song.objects.get(pk=pk)
    except Song.DoesNotExist:
        return Response({'error': 'Song not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = SongSerializer(song)
    return Response(serializer.data)


@api_view(['GET'])
def api_chords(request):
    """Return all chords, optionally filtered by difficulty or category.

    GET parameters:
        difficulty: filter by difficulty level
        category: filter by chord category
    """
    difficulty = request.GET.get('difficulty', '')
    category = request.GET.get('category', '')

    chords = Chord.objects.all()
    if difficulty:
        chords = chords.filter(difficulty=difficulty)
    if category:
        chords = chords.filter(category=category)

    serializer = ChordSerializer(chords, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_chord_detail(request, pk):
    """Return a single chord by its ID."""
    try:
        chord = Chord.objects.get(pk=pk)
    except Chord.DoesNotExist:
        return Response({'error': 'Chord not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ChordSerializer(chord)
    return Response(serializer.data)


@api_view(['GET'])
def api_tabs(request):
    """Return all tabs, optionally filtered by song.

    GET parameters:
        song: filter tabs by song ID
    """
    song_id = request.GET.get('song', '')
    if song_id:
        tabs = Tab.objects.filter(song_id=song_id)
    else:
        tabs = Tab.objects.all()
    serializer = TabSerializer(tabs, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def api_tab_detail(request, pk):
    """Return a single tab by its ID."""
    try:
        tab = Tab.objects.get(pk=pk)
    except Tab.DoesNotExist:
        return Response({'error': 'Tab not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = TabSerializer(tab)
    return Response(serializer.data)


@api_view(['GET'])
def api_featured(request):
    """Return the featured tab (highest quality score) for the home screen."""
    tabs = Tab.objects.all()
    if tabs:
        tab = tabs.order_by('-quality_score').first()
        serializer = TabSerializer(tab)
        return Response(serializer.data)
    else:
        return Response({'error': 'No tabs available'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def api_search(request):
    """Search songs and tabs by query string.

    GET parameters:
        q: search string

    Returns:
        JSON with 'songs' and 'tabs' arrays
    """
    query = request.GET.get('q', '')
    if not query:
        return Response({'songs': [], 'tabs': []})

    songs = Song.objects.filter(Q(title__icontains=query) | Q(artist__icontains=query))[:10]
    tabs = Tab.objects.filter(
        Q(song__title__icontains=query) | Q(song__artist__icontains=query)
    )[:10]

    return Response({
        'songs': SongSerializer(songs, many=True).data,
        'tabs': TabSerializer(tabs, many=True).data
    })
