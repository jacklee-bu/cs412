from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import HttpResponse
from .models import Profile

# Create your views here.

class ProfileListView(ListView):
    model = Profile
    template_name = 'mini_insta/show_all_profiles.html'
    context_object_name = 'profiles'

def show_profile(request, pk):
    # print("Debug: showing profile", pk)  # left this here for debugging
    profile_obj = get_object_or_404(Profile, pk=pk)
    context = {'profile': profile_obj}
    return render(request, 'mini_insta/show_profile.html', context)
