# Jack Lee
# jacklee@bu.edu
# views.py for mini_insta app - handles web page rendering and form processing

from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from django.urls import reverse
from .models import Profile, Post, Photo
from .forms import CreatePostForm

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
        """Add profile to context for template rendering.
        Returns: context dictionary with profile object
        """
        # need to pass the profile to the template
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """Process valid form submission.
        Sets profile foreign key and creates associated photo.
        Returns: redirect response to post detail page
        """
        # set the profile before saving the post
        profile = Profile.objects.get(pk=self.kwargs['pk'])
        form.instance.profile = profile

        # save the post first
        response = super().form_valid(form)

        # now create the photo if url was provided
        image_url = self.request.POST.get('image_url')
        if image_url:
            photo = Photo(post=form.instance, image_url=image_url)
            photo.save()

        return response

    def get_success_url(self):
        """Get URL to redirect to after successful post creation.
        Returns: URL string for post detail page
        """
        # redirect to the post detail page after creation
        return reverse('mini_insta:post_detail', kwargs={'pk': self.object.pk})
