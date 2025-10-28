from django.shortcuts import render

# Create your views here.

def home(request):
    """Home view for the recipe app."""
    return render(request, 'recipe/recipes_home.html')
