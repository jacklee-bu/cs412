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
            'image_url': 'https://dl-asset.cyberlink.com/web/prog/learning-center/html/39109/PDR19-YouTube-953_Funny_Cat_Video/img/ai_cat_trend.jpg',
            'name': 'Jack'
        },
        {
            'image_url': 'https://static.vecteezy.com/system/resources/previews/029/552/826/large_2x/portraits-of-cats-funny-faces-generative-ai-photo.jpg',
            'name': 'Jack'
        },
        {
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ_uWusOjEY9AeK2aIubHYCWA2RZ3zSl39LmA&s',
            'name': 'Jack'
        },
        {
            'image_url': 'https://cdn.pixabay.com/photo/2025/06/11/13/19/ai-generated-9654480_1280.png',
            'name': 'Jack'
        },
        {
            'image_url': 'https://previews.123rf.com/images/9process/9process2312/9process231200293/220306638-funny-ginger-cat-with-orange-glasses-and-collar-on-blue-background-ai-generated.jpg',
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
