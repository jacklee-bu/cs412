# File: views.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: November 2025
# Description: Views for dadjokes app

from django.shortcuts import render, get_object_or_404
from .models import Joke, Picture
import random

def random_view(request):
    jokes = Joke.objects.all()
    pictures = Picture.objects.all()

    joke = random.choice(jokes) if jokes else None
    picture = random.choice(pictures) if pictures else None

    context = {
        'joke': joke,
        'picture': picture,
    }

    return render(request, 'dadjokes/random.html', context)


def jokes_view(request):
    jokes = Joke.objects.all()
    context = {
        'jokes': jokes,
    }
    return render(request, 'dadjokes/jokes.html', context)


def joke_detail(request, pk):
    joke = get_object_or_404(Joke, pk=pk)
    context = {
        'joke': joke,
    }
    return render(request, 'dadjokes/joke_detail.html', context)


def pictures_view(request):
    pictures = Picture.objects.all()
    context = {
        'pictures': pictures,
    }
    return render(request, 'dadjokes/pictures.html', context)


def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    context = {
        'picture': picture,
    }
    return render(request, 'dadjokes/picture_detail.html', context)
