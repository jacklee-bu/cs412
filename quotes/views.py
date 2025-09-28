from django.shortcuts import render
import random

# Lists of quotes and images for Albert Einstein
quotes = [
    "Imagination is more important than knowledge. For knowledge is limited, whereas imagination embraces the entire world, stimulating progress, giving birth to evolution.",
    "The important thing is not to stop questioning. Curiosity has its own reason for existing.",
    "Try not to become a person of success, but rather try to become a person of value.",
    "Life is like riding a bicycle. To keep your balance, you must keep moving.",
    "Logic will get you from A to B. Imagination will take you everywhere.",
]

images = [
    "https://upload.wikimedia.org/wikipedia/commons/d/d3/Albert_Einstein_Head.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f5/Einstein_1921_by_F_Schmutzer_2.jpg/256px-Einstein_1921_by_F_Schmutzer_2.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/1/14/Albert_Einstein_1947.jpg/256px-Albert_Einstein_1947.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/5/50/Albert_Einstein_%28Nobel%29.png",
    "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3e/Einstein_1921_by_F_Schmutzer_-_restoration.jpg/256px-Einstein_1921_by_F_Schmutzer_-_restoration.jpg",
]

def quote(request):
    """Display a random quote and image."""
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)
    
    context = {
        'quote': selected_quote,
        'image': selected_image,
    }
    
    return render(request, 'quotes/quote.html', context)

def show_all(request):
    """Display all quotes and images."""
    context = {
        'quotes': quotes,
        'images': images,
    }
    
    return render(request, 'quotes/show_all.html', context)

def about(request):
    """Display information about Einstein and the creator."""
    return render(request, 'quotes/about.html')
