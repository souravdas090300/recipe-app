from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
# To protect class-based views
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def home(request):
    """Home view for the recipe app."""
    return render(request, 'recipe/recipes_home.html')


class RecipeListView(LoginRequiredMixin, ListView):
    """Protected list view showing all recipes with their images."""
    model = Recipe
    template_name = 'recipe/recipes_list.html'


class RecipeDetailView(LoginRequiredMixin, DetailView):
    """Protected detail view for a single recipe, including computed difficulty."""
    model = Recipe
    template_name = 'recipe/recipe_detail.html'

