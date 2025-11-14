# File: models.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: November 2025
# Description: Models for dadjokes app to store jokes and silly pictures

from django.db import models

class Joke(models.Model):
    text = models.TextField()
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.text[:50]}..."


class Picture(models.Model):
    image_url = models.URLField(max_length=500)
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}: {self.image_url}"


def load_data():
    Joke.objects.all().delete()
    Picture.objects.all().delete()

    jokes_data = [
        {
            'text': "Why don't eggs tell jokes? They'd crack each other up.",
            'name': 'Jack'
        },
        {
            'text': "I used to hate facial hair, but then it grew on me.",
            'name': 'Jack'
        },
        {
            'text': "What do you call a fish wearing a bowtie? Sofishticated.",
            'name': 'Jack'
        },
        {
            'text': "I'm reading a book about anti-gravity. It's impossible to put down.",
            'name': 'Jack'
        },
        {
            'text': "Did you hear about the claustrophobic astronaut? He just needed a little space.",
            'name': 'Jack'
        },
        {
            'text': "Why don't scientists trust atoms? Because they make up everything.",
            'name': 'Jack'
        },
        {
            'text': "How does a penguin build its house? Igloos it together.",
            'name': 'Jack'
        },
    ]

    pictures_data = [
        {
            'image_url': 'https://media.giphy.com/media/ICOgUNjpvO0PC/giphy.gif',
            'name': 'Jack'
        },
        {
            'image_url': 'https://media.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif',
            'name': 'Jack'
        },
        {
            'image_url': 'https://media.giphy.com/media/mlvseq9yvZhba/giphy.gif',
            'name': 'Jack'
        },
        {
            'image_url': 'https://media.giphy.com/media/l3q2K5jinAlChoCLS/giphy.gif',
            'name': 'Jack'
        },
        {
            'image_url': 'https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif',
            'name': 'Jack'
        },
        {
            'image_url': 'https://media.giphy.com/media/IcGkqdUmYLFGE/giphy.gif',
            'name': 'Jack'
        },
    ]

    for joke_data in jokes_data:
        joke = Joke(
            text=joke_data['text'],
            name=joke_data['name']
        )
        joke.save()

    for picture_data in pictures_data:
        picture = Picture(
            image_url=picture_data['image_url'],
            name=picture_data['name']
        )
        picture.save()

    print(f"Successfully loaded {len(jokes_data)} jokes and {len(pictures_data)} pictures.")
