from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe

# Create your views here.

def home(request):
    """Home view for the recipe app."""
    return render(request, 'recipe/recipes_home.html')


class RecipeListView(ListView):
    """List view showing all recipes with their images."""
    model = Recipe
    template_name = 'recipe/recipes_list.html'


class RecipeDetailView(DetailView):
    """Detail view for a single recipe, including computed difficulty."""
    model = Recipe
    template_name = 'recipe/recipe_detail.html'
