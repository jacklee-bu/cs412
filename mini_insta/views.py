# Jack Lee
# jacklee@bu.edu
# views.py for mini_insta app - handles web page rendering and form processing

from django.shortcuts import render, get_object_or_404
from django.views.generic import (ListView, DetailView, CreateView,
                                  UpdateView, DeleteView)
from django.http import HttpResponse
from django.urls import reverse
from .models import Profile, Post, Photo
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
