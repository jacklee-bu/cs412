# Jack Lee
# jacklee@bu.edu
# views.py for mini_insta app - handles web page rendering and form processing

from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView, TemplateView)
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import models
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Profile, Post, Photo, Follow, Comment, Like
from .forms import CreatePostForm, UpdateProfileForm, UpdatePostForm, CreateProfileForm

# Create your views here.

class AuthenticatedView(LoginRequiredMixin):
    """Custom mixin for views requiring authentication."""

    def get_login_url(self):
        """Get the login URL.
        Returns: URL string
        """
        # return the mini_insta specific login URL
        return reverse('mini_insta:login')

    def get_profile_for_user(self):
        """Get the Profile for the logged in user.
        Returns: Profile object or None
        """
        # get the profile for the logged in user
        try:
            profile = Profile.objects.get(user=self.request.user)
            return profile
        except Profile.DoesNotExist:
            return None
        except Profile.MultipleObjectsReturned:
            # multiple profiles for admin user - get first one
            return Profile.objects.filter(user=self.request.user).first()

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
    context = {'profile': profile_obj, 'is_following_profile': False}

    # add the logged in user's profile if authenticated
    if request.user.is_authenticated:
        try:
            logged_in_profile = Profile.objects.get(user=request.user)
            context['logged_in_profile'] = logged_in_profile
            if logged_in_profile != profile_obj:
                context['is_following_profile'] = logged_in_profile.is_following(profile_obj)
        except Profile.DoesNotExist:
            pass

    return render(request, 'mini_insta/show_profile.html', context)

class PostDetailView(DetailView):
    """View to display a single post with all its photos."""
    model = Post
    template_name = 'mini_insta/show_post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        """Add logged in profile to context.
        Returns: context dictionary
        """
        context = super().get_context_data(**kwargs)

        # add the logged in user's profile if authenticated
        if self.request.user.is_authenticated:
            try:
                logged_in_profile = Profile.objects.get(user=self.request.user)
                context['logged_in_profile'] = logged_in_profile
            except Profile.DoesNotExist:
                pass

        return context

class CreatePostView(AuthenticatedView, CreateView):
    """View to handle creating a new post with photos."""
    form_class = CreatePostForm
    template_name = 'mini_insta/create_post_form.html'

    def get_context_data(self, **kwargs):
        """Add profile to context.
        Returns: context dictionary
        """
        # need to pass profile to template
        context = super().get_context_data(**kwargs)
        profile = self.get_profile_for_user()
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """Process valid form submission.
        Returns: redirect response
        """
        profile = self.get_profile_for_user()
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

class UpdateProfileView(AuthenticatedView, UpdateView):
    """View to handle updating an existing profile."""
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_insta/update_profile_form.html'

    def get_object(self):
        """Get the Profile for the logged in user.
        Returns: Profile object
        """
        # get the profile for the logged in user
        return self.get_profile_for_user()

class DeletePostView(AuthenticatedView, DeleteView):
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

class UpdatePostView(AuthenticatedView, UpdateView):
    """View to handle updating a post."""
    model = Post
    form_class = UpdatePostForm
    template_name = 'mini_insta/update_post_form.html'

class ShowOwnProfileView(AuthenticatedView, DetailView):
    """View to display the logged-in user's own profile."""
    model = Profile
    template_name = 'mini_insta/show_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        """Get the Profile for the logged in user.
        Returns: Profile object
        """
        # get the profile for the logged in user
        return self.get_profile_for_user()

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

class PostFeedListView(AuthenticatedView, ListView):
    """View to display the post feed for a profile."""
    model = Post
    template_name = 'mini_insta/show_feed.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Get the post feed for the profile.
        Returns: QuerySet of Post objects
        """
        # get the profile for the logged in user
        profile = self.get_profile_for_user()
        # use the get_post_feed method we created
        return profile.get_post_feed()

    def get_context_data(self, **kwargs):
        """Add profile to context.
        Returns: context dictionary
        """
        context = super().get_context_data(**kwargs)
        # add the profile to context for template use
        context['profile'] = self.get_profile_for_user()
        return context

class SearchView(AuthenticatedView, ListView):
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
            profile = self.get_profile_for_user()
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
        profile = self.get_profile_for_user()
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

class LogoutConfirmationView(TemplateView):
    """View to display logout confirmation page."""
    template_name = 'mini_insta/logged_out.html'

class CreateProfileView(TemplateView):
    """View to handle creating a new profile with user registration."""
    template_name = 'mini_insta/create_profile_form.html'

    def get_context_data(self, **kwargs):
        """Add UserCreationForm to context.
        Returns: context dictionary
        """
        context = super().get_context_data(**kwargs)
        # include the profile form with a prefix to avoid collisions with the User form
        form = context.get('form')
        if form is None:
            if self.request.method == 'POST':
                form = CreateProfileForm(self.request.POST, prefix='profile')
            else:
                form = CreateProfileForm(prefix='profile')
        context['form'] = form

        # include the user creation form, reusing any bound form passed via kwargs
        user_form = context.get('user_form')
        if user_form is None:
            if self.request.method == 'POST':
                user_form = UserCreationForm(self.request.POST, prefix='user')
            else:
                user_form = UserCreationForm(prefix='user')
        context['user_form'] = user_form
        return context

    def post(self, request, *args, **kwargs):
        """Handle form submission for account creation + profile setup."""
        profile_form = CreateProfileForm(request.POST, prefix='profile')
        user_form = UserCreationForm(request.POST, prefix='user')

        if profile_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            return HttpResponseRedirect(
                reverse('mini_insta:show_profile', kwargs={'pk': profile.pk})
            )

        context = self.get_context_data(form=profile_form, user_form=user_form)
        return self.render_to_response(context)

class FollowProfileView(AuthenticatedView, TemplateView):
    """View to handle following a profile."""

    def dispatch(self, request, *args, **kwargs):
        """Handle the follow operation.
        Returns: redirect response
        """
        # get the profile to follow
        profile_to_follow = get_object_or_404(Profile, pk=self.kwargs['pk'])
        # get the logged in user's profile
        follower_profile = self.get_profile_for_user()

        # dont allow self-following
        if profile_to_follow != follower_profile:
            # check if not already following
            if not Follow.objects.filter(profile=profile_to_follow,
                                        follower_profile=follower_profile).exists():
                # create the follow relationship
                follow = Follow(profile=profile_to_follow, follower_profile=follower_profile)
                follow.save()

        # redirect back to the profile page
        return HttpResponseRedirect(reverse('mini_insta:show_profile',
                                          kwargs={'pk': profile_to_follow.pk}))

class UnfollowProfileView(AuthenticatedView, TemplateView):
    """View to handle unfollowing a profile."""

    def dispatch(self, request, *args, **kwargs):
        """Handle the unfollow operation.
        Returns: redirect response
        """
        # get the profile to unfollow
        profile_to_unfollow = get_object_or_404(Profile, pk=self.kwargs['pk'])
        # get the logged in user's profile
        follower_profile = self.get_profile_for_user()

        # delete the follow relationship if it exists
        Follow.objects.filter(profile=profile_to_unfollow,
                            follower_profile=follower_profile).delete()

        # redirect back to the profile page
        return HttpResponseRedirect(reverse('mini_insta:show_profile',
                                          kwargs={'pk': profile_to_unfollow.pk}))

class LikePostView(AuthenticatedView, TemplateView):
    """View to handle liking a post."""

    def dispatch(self, request, *args, **kwargs):
        """Handle the like operation.
        Returns: redirect response
        """
        # get the post to like
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # get the logged in user's profile
        profile = self.get_profile_for_user()

        # dont allow liking own posts
        if post.profile != profile:
            # check if not already liked
            if not Like.objects.filter(post=post, profile=profile).exists():
                # create the like
                like = Like(post=post, profile=profile)
                like.save()

        # redirect back to the post page
        return HttpResponseRedirect(reverse('mini_insta:post_detail',
                                          kwargs={'pk': post.pk}))

class UnlikePostView(AuthenticatedView, TemplateView):
    """View to handle unliking a post."""

    def dispatch(self, request, *args, **kwargs):
        """Handle the unlike operation.
        Returns: redirect response
        """
        # get the post to unlike
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # get the logged in user's profile
        profile = self.get_profile_for_user()

        # delete the like if it exists
        Like.objects.filter(post=post, profile=profile).delete()

        # redirect back to the post page
        return HttpResponseRedirect(reverse('mini_insta:post_detail',
                                          kwargs={'pk': post.pk}))
