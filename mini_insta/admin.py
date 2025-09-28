from django.contrib import admin
from .models import Profile

# Register your models here.

# tried to customize the admin but couldn't get it to work
# class ProfileAdmin(admin.ModelAdmin):
#     list_display = ['username', 'display_name']
#     search_fields = ['username']

admin.site.register(Profile)
# admin.site.register(Profile, ProfileAdmin)  # commented out for now
