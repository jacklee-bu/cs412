# File: views.py
# Author: Jack Lee (jacklee@bu.edu)
# Date: December 2025
# Description: Views for the guitar tabs application (tabby).
#              Handles all web page rendering and form processing.

from django.shortcuts import redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from .models import Song, Chord, Tab, UserFavorite, Exercise
from .forms import SongForm, ChordForm, TabForm, UserFavoriteForm
import random


class RegisterView(CreateView):
    """Handle user registration with automatic login after signup."""
    form_class = UserCreationForm
    template_name = 'project/register.html'
    success_url = reverse_lazy('project:home')

    def form_valid(self, form):
        """Save the new user and log them in automatically."""
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class LogoutView(TemplateView):
    """Handle user logout with GET showing confirm page, POST doing logout."""
    template_name = 'project/logout_confirm.html'

    def post(self, request):
        """Process the logout and redirect to home."""
        logout(request)
        return redirect('project:home')


class HomeView(TemplateView):
    """Display the home page with featured content."""
    template_name = 'project/home.html'

    def get_context_data(self, **kwargs):
        """Add featured tab, recent tabs, beginner chords, and random exercise."""
        context = super().get_context_data(**kwargs)
        context['featured_tab'] = Tab.objects.order_by('-quality_score').first()
        context['recent_tabs'] = Tab.objects.order_by('-date_fetched')[:6]
        context['beginner_chords'] = Chord.objects.filter(difficulty='beginner')[:7]
        exercises = list(Exercise.objects.all())
        context['random_exercise'] = random.choice(exercises) if exercises else None
        return context


class TunerView(TemplateView):
    """Display the guitar tuner page."""
    template_name = 'project/tuner.html'


class ExerciseListView(ListView):
    """Display all exercises with optional filtering by category/difficulty."""
    model = Exercise
    template_name = 'project/exercise_list.html'
    context_object_name = 'exercises'

    def get_queryset(self):
        """Filter exercises based on GET parameters."""
        queryset = Exercise.objects.all()
        category = self.request.GET.get('category', '')
        difficulty = self.request.GET.get('difficulty', '')
        if category:
            queryset = queryset.filter(category=category)
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset

    def get_context_data(self, **kwargs):
        """Add filter choices and selected values to context."""
        context = super().get_context_data(**kwargs)
        context['categories'] = Exercise.CATEGORY_CHOICES
        context['difficulties'] = Exercise.DIFFICULTY_CHOICES
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        return context


class ExerciseDetailView(DetailView):
    """Display a single exercise with all its details."""
    model = Exercise
    template_name = 'project/exercise_detail.html'
    context_object_name = 'exercise'


class ExerciseCreateView(CreateView):
    """Handle creating a new exercise."""
    model = Exercise
    fields = ['name', 'description', 'instructions', 'category', 'difficulty', 'duration_minutes', 'tab_notation', 'tips']
    template_name = 'project/exercise_form.html'


class ExerciseUpdateView(UpdateView):
    """Handle editing an existing exercise."""
    model = Exercise
    fields = ['name', 'description', 'instructions', 'category', 'difficulty', 'duration_minutes', 'tab_notation', 'tips']
    template_name = 'project/exercise_form.html'


class ExerciseDeleteView(DeleteView):
    """Handle deleting an exercise."""
    model = Exercise
    template_name = 'project/exercise_confirm_delete.html'
    success_url = reverse_lazy('project:exercise_list')


class SongListView(ListView):
    """Display all songs with search and sorting options."""
    model = Song
    template_name = 'project/song_list.html'
    context_object_name = 'songs'
    paginate_by = 20

    def get_queryset(self):
        """Filter songs by search query and apply sorting."""
        queryset = Song.objects.all()
        q = self.request.GET.get('q', '')
        if q:
            queryset = queryset.filter(Q(title__icontains=q) | Q(artist__icontains=q))
        sort = self.request.GET.get('sort', 'title')
        if sort == 'artist':
            queryset = queryset.order_by('artist', 'title')
        elif sort == 'recent':
            queryset = queryset.order_by('-date_added')
        else:
            queryset = queryset.order_by('title')
        return queryset

    def get_context_data(self, **kwargs):
        """Add search query, sort option, and total count to context."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        context['current_sort'] = self.request.GET.get('sort', 'title')
        context['total_count'] = self.get_queryset().count()
        return context


class SongDetailView(DetailView):
    """Display a single song with its tabs."""
    model = Song
    template_name = 'project/song_detail.html'
    context_object_name = 'song'


class SongCreateView(CreateView):
    """Handle creating a new song."""
    model = Song
    form_class = SongForm
    template_name = 'project/song_form.html'


class SongUpdateView(UpdateView):
    """Handle editing an existing song."""
    model = Song
    form_class = SongForm
    template_name = 'project/song_form.html'


class SongDeleteView(DeleteView):
    """Handle deleting a song."""
    model = Song
    template_name = 'project/song_confirm_delete.html'
    success_url = reverse_lazy('project:song_list')


class ChordListView(ListView):
    """Display all chords with optional filtering."""
    model = Chord
    template_name = 'project/chord_list.html'
    context_object_name = 'chords'

    def get_queryset(self):
        """Filter chords by difficulty or category."""
        queryset = Chord.objects.all()
        difficulty = self.request.GET.get('difficulty', '')
        category = self.request.GET.get('category', '')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        """Add filter choices and selected values to context."""
        context = super().get_context_data(**kwargs)
        context['difficulties'] = ['beginner', 'intermediate', 'advanced', 'expert']
        context['categories'] = [c[0] for c in Chord.CATEGORY_CHOICES]
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class ChordDetailView(DetailView):
    """Display a single chord with its fingering diagram."""
    model = Chord
    template_name = 'project/chord_detail.html'
    context_object_name = 'chord'


class ChordCreateView(CreateView):
    """Handle creating a new chord."""
    model = Chord
    form_class = ChordForm
    template_name = 'project/chord_form.html'


class ChordUpdateView(UpdateView):
    """Handle editing an existing chord."""
    model = Chord
    form_class = ChordForm
    template_name = 'project/chord_form.html'


class ChordDeleteView(DeleteView):
    """Handle deleting a chord."""
    model = Chord
    template_name = 'project/chord_confirm_delete.html'
    success_url = reverse_lazy('project:chord_list')


class TabListView(ListView):
    """Display all tabs with optional difficulty filtering."""
    model = Tab
    template_name = 'project/tab_list.html'
    context_object_name = 'tabs'
    paginate_by = 20

    def get_queryset(self):
        """Filter tabs by difficulty if specified."""
        queryset = Tab.objects.all()
        difficulty = self.request.GET.get('difficulty', '')
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        return queryset

    def get_context_data(self, **kwargs):
        """Add selected difficulty to context."""
        context = super().get_context_data(**kwargs)
        context['selected_difficulty'] = self.request.GET.get('difficulty', '')
        return context


class TabDetailView(DetailView):
    """Display a tab with full content and chord data for tooltips."""
    model = Tab
    template_name = 'project/tab_detail.html'
    context_object_name = 'tab'

    def get_context_data(self, **kwargs):
        """Add chord fingering data as JSON for the tooltip feature."""
        context = super().get_context_data(**kwargs)
        import json
        chords = Chord.objects.all()
        context['chord_data_json'] = json.dumps({c.name: c.fingering for c in chords})
        return context


class TabCreateView(CreateView):
    """Handle creating a new tab."""
    model = Tab
    form_class = TabForm
    template_name = 'project/tab_form.html'

    def get_initial(self):
        """Pre-fill the song field if song ID is in the URL."""
        initial = super().get_initial()
        song_id = self.request.GET.get('song')
        if song_id:
            initial['song'] = song_id
        return initial


class TabUpdateView(UpdateView):
    """Handle editing an existing tab."""
    model = Tab
    form_class = TabForm
    template_name = 'project/tab_form.html'


class TabDeleteView(DeleteView):
    """Handle deleting a tab."""
    model = Tab
    template_name = 'project/tab_confirm_delete.html'

    def get_success_url(self):
        """Redirect to the song detail page after deletion."""
        return reverse('project:song_detail', kwargs={'pk': self.object.song.pk})


class FavoriteListView(LoginRequiredMixin, ListView):
    """Display the logged-in user's favorite tabs."""
    model = UserFavorite
    template_name = 'project/favorite_list.html'
    context_object_name = 'favorites'
    login_url = 'project:login'

    def get_queryset(self):
        """Return only favorites belonging to the current user."""
        return UserFavorite.objects.filter(user=self.request.user)


class FavoriteCreateView(LoginRequiredMixin, CreateView):
    """Handle adding a tab to the user's favorites."""
    model = UserFavorite
    form_class = UserFavoriteForm
    template_name = 'project/favorite_form.html'
    login_url = 'project:login'

    def form_valid(self, form):
        """Set the user to the currently logged-in user before saving."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        """Redirect to favorites list after adding."""
        return reverse('project:favorite_list')


class FavoriteUpdateView(LoginRequiredMixin, UpdateView):
    """Handle updating notes on a favorite."""
    model = UserFavorite
    form_class = UserFavoriteForm
    template_name = 'project/favorite_form.html'
    login_url = 'project:login'

    def get_queryset(self):
        """Only allow editing the current user's favorites."""
        return UserFavorite.objects.filter(user=self.request.user)


class FavoriteDeleteView(LoginRequiredMixin, DeleteView):
    """Handle removing a tab from favorites."""
    model = UserFavorite
    template_name = 'project/favorite_confirm_delete.html'
    success_url = reverse_lazy('project:favorite_list')
    login_url = 'project:login'

    def get_queryset(self):
        """Only allow deleting the current user's favorites."""
        return UserFavorite.objects.filter(user=self.request.user)
