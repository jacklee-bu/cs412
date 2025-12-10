# File: models.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: December 2025
# Description: Data models for the guitar tabs application (tabby).
#              Defines Song, Chord, Tab, Exercise, and UserFavorite models.

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Song(models.Model):
    """A song that can have guitar tabs associated with it."""
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return string representation of the song."""
        return f'{self.title} - {self.artist}'

    def get_absolute_url(self):
        """Return the URL for this song's detail page."""
        return reverse('project:song_detail', kwargs={'pk': self.pk})


class Chord(models.Model):
    """A guitar chord with fingering information.

    This model can stand alone without foreign keys.
    """
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]

    CATEGORY_CHOICES = [
        ('major', 'Major'),
        ('minor', 'Minor'),
        ('seventh', 'Seventh'),
        ('major_seventh', 'Major Seventh'),
        ('minor_seventh', 'Minor Seventh'),
        ('suspended', 'Suspended'),
        ('augmented', 'Augmented'),
        ('diminished', 'Diminished'),
        ('power', 'Power Chord'),
        ('barre', 'Barre Chord'),
        ('other', 'Other'),
    ]

    name = models.CharField(max_length=20, unique=True)
    full_name = models.CharField(max_length=100)
    fingering = models.CharField(max_length=20)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='major')
    image = models.ImageField(upload_to='chord_diagrams/', null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        """Return string representation of the chord."""
        return f'{self.name} ({self.full_name})'

    def get_absolute_url(self):
        """Return the URL for this chord's detail page."""
        return reverse('project:chord_detail', kwargs={'pk': self.pk})


class Tab(models.Model):
    """A guitar tab for a song.

    Requires a foreign key to Song - every tab must belong to a song.
    """
    TUNING_CHOICES = [
        ('standard', 'Standard (EADGBE)'),
        ('drop_d', 'Drop D (DADGBE)'),
        ('half_step_down', 'Half Step Down'),
        ('full_step_down', 'Full Step Down'),
        ('open_g', 'Open G'),
        ('open_d', 'Open D'),
        ('dadgad', 'DADGAD'),
        ('other', 'Other'),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='tabs')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    content = models.TextField()
    chords_used = models.CharField(max_length=500, blank=True)
    strumming_pattern = models.CharField(max_length=200, blank=True)
    tuning = models.CharField(max_length=20, choices=TUNING_CHOICES, default='standard')
    capo = models.IntegerField(default=0)
    tempo = models.IntegerField(null=True, blank=True)
    source_url = models.URLField(blank=True)
    source_site = models.CharField(max_length=100, blank=True)
    quality_score = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)
    date_fetched = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-quality_score', '-rating_count']

    def __str__(self):
        """Return string representation of the tab."""
        return f'Tab for {self.song.title} ({self.source_site or "unknown"})'

    def get_absolute_url(self):
        """Return the URL for this tab's detail page."""
        return reverse('project:tab_detail', kwargs={'pk': self.pk})

    def get_chords_list(self):
        """Parse the chords_used field into a list of chord names."""
        if self.chords_used:
            return [c.strip() for c in self.chords_used.split(',')]
        return []


class Exercise(models.Model):
    """A guitar practice exercise.

    Has a many-to-many relationship with Chord for exercises
    that focus on specific chords.
    """
    CATEGORY_CHOICES = [
        ('finger', 'Finger Exercises'),
        ('chord_transition', 'Chord Transitions'),
        ('picking', 'Picking Patterns'),
        ('strumming', 'Strumming Patterns'),
        ('scales', 'Scales'),
        ('stretching', 'Hand Stretching'),
        ('rhythm', 'Rhythm Training'),
    ]

    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    instructions = models.TextField(help_text='Step-by-step instructions')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='finger')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    duration_minutes = models.IntegerField(default=5)
    tab_notation = models.TextField(blank=True, help_text='Optional tablature')
    tips = models.TextField(blank=True)
    chords = models.ManyToManyField(Chord, blank=True, related_name='exercises')
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['category', 'difficulty', 'name']

    def __str__(self):
        """Return string representation of the exercise."""
        return f'{self.name} ({self.get_category_display()})'

    def get_absolute_url(self):
        """Return the URL for this exercise's detail page."""
        return reverse('project:exercise_detail', kwargs={'pk': self.pk})


class UserFavorite(models.Model):
    """A user's saved/favorite tab with practice tracking.

    Requires two foreign keys: User and Tab.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, related_name='favorited_by')
    date_saved = models.DateTimeField(auto_now_add=True)
    practice_time = models.IntegerField(default=0)
    last_practiced = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_mastered = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date_saved']
        unique_together = ['user', 'tab']

    def __str__(self):
        """Return string representation of the favorite."""
        return f'{self.user.username} - {self.tab.song.title}'

    def get_absolute_url(self):
        """Return the URL for the favorites list."""
        return reverse('project:favorite_list')
