# Jack Lee
# jacklee@bu.edu
# views.py for mini_insta app - handles web page rendering and form processing

from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import models
from .models import Profile, Post, Photo, Follow, Comment, Like
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm

# Create your views here.

class ProfileListView(ListView):
    """View to display list of all profiles."""
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

def show_profile(request, pk):
    """Display a single profile page.
    Args: pk - primary key of the Profile to display
    Returns: rendered show_profile.html template
    """
    # print("Debug: showing profile", pk)  # left this here for debugging
    profile_obj = get_object_or_404(Profile, pk=pk)
    context = {'profile': profile_obj}
    return render(request, 'mini_insta/show_profile.html', context)

class PostDetailView(DetailView):
    """View to display a single post with all its photos."""
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

class CreatePostView(CreateView):
    """View to handle creating a new post with photos."""
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        """Add profile to context.
        Returns: context dictionary
        """
        # need to pass profile to template
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """Process valid form submission.
        Returns: redirect response
        """
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile

        response = super().form_valid(form)

        # handle file uploads
        files = self.request.FILES.getlist('files')
        # create a photo for each uploaded file
        for file in files:
            photo = Photo(post=form.instance, image_file=file)
            photo.save()

        return response

    def get_success_url(self):
        """Get URL to redirect to after successful post creation.
        Returns: URL string
        """
        return reverse('mini_insta:post_detail',
                      kwargs={'pk': self.object.pk})

class UpdateProfileView(UpdateView):
    """View to handle updating an existing profile."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

class DeletePostView(DeleteView):
    """View to handle deleting a post."""
    model = Post
    template_name = 'mini_insta/delete_post_form.html'

    def get_context_data(self, **kwargs):
        """Add post and profile to context.
        Returns: context dictionary
        """
        context = super().get_context_data(**kwargs)
        context['post'] = self.object
        context['profile'] = self.object.profile
        return context

    def get_success_url(self):
        """Get URL to redirect to after delete.
        Returns: URL string
        """
        return reverse('mini_insta:show_profile',
                      kwargs={'pk': self.object.profile.pk})

class UpdatePostView(UpdateView):
    """View to handle updating a post."""
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

class ShowFollowersDetailView(DetailView):
    """View to display followers of a profile."""
    model = Profile
    template_name = 'mini_insta/show_followers.html'
    context_object_name = 'profile'

class ShowFollowingDetailView(DetailView):
    """View to display profiles being followed."""
    model = Profile
    template_name = 'mini_insta/show_following.html'
    context_object_name = 'profile'

class PostFeedListView(ListView):
    """View to display the post feed for a profile."""
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Get the post feed for the profile.
        Returns: QuerySet of Post objects
        """
        # get the profile from the URL
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        # use the get_post_feed method we created
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """Add profile to context.
        Returns: context dictionary
        """
        context = super().get_context_data(**kwargs)
        # add the profile to context for template use
        context['profile'] = Profile.objects.get(pk=self.kwargs['pk'])
        return context

class SearchView(ListView):
    """View to handle search functionality."""
    model = Post
    template_name = 'mini_insta/search_results.html'
    context_object_name = 'posts'

    def dispatch(self, request, *args, **kwargs):
        """Handle initial request dispatch.
        Returns: response object
        """
        # check if there's a query parameter
        if 'query' not in self.request.GET:
            # no query, show the search form
            profile = Profile.objects.get(pk=self.kwargs['pk'])
            context = {'profile': profile}
            return render(request, 'mini_insta/search.html', context)
        # otherwise continue with normal ListView processing
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Get posts matching the search query.
        Returns: QuerySet of Post objects
        """
        # get the search query
        query = self.request.GET.get('query', '')
        # search for posts with query in caption
        posts = Post.objects.filter(caption__icontains=query)
        return posts

    def get_context_data(self, **kwargs):
        """Add additional context data.
        Returns: context dictionary
        """
        context = super().get_context_data(**kwargs)
        # get the profile and query
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        query = self.request.GET.get('query', '')

        # search for matching profiles
        profiles = Profile.objects.filter(
            models.Q(username__icontains=query) |
            models.Q(display_name__icontains=query) |
            models.Q(bio_text__icontains=query)
        )

        # add to context
        context['profile'] = profile
        context['query'] = query
        context['profiles'] = profiles
        # posts are already in context from get_queryset

        return context
