from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Recipe
# To protect class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
# Import for search functionality
from .forms import RecipeSearchForm
import pandas as pd
from .utils import get_chart

# Create your views here.

def home(request):
    """Home view for the recipe app."""
    return render(request, 'recipe/recipes_home.html')


def about(request):
    """About page for the recipe app."""
    return render(request, 'recipe/about.html')


class RecipeListView(LoginRequiredMixin, ListView):
    """Protected list view showing all recipes with their images and search functionality."""
    model = Recipe
    template_name = 'recipe/recipes_list.html'
    
    def post(self, request, *args, **kwargs):
        """Handle POST requests for search functionality."""
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """Add search form and results to context."""
        context = super().get_context_data(**kwargs)
        
        # Support both POST (form submit) and GET (homepage search/navigation)
        if self.request.method == 'POST':
            data = self.request.POST
        elif self.request.method == 'GET':
            data = self.request.GET
        else:
            data = None

        # Create an instance of RecipeSearchForm
        form = RecipeSearchForm(data or None)
        context['form'] = form
        
        # Initialize variables
        recipes_df = None
        chart = None
        
        # Check if form was submitted
        if self.request.method in ['POST', 'GET'] and form.is_valid():
            # Get search criteria
            recipe_name = data.get('recipe_name')
            chart_type = data.get('chart_type')
            difficulty = data.get('difficulty')
            
            # Start with all recipes
            qs = Recipe.objects.all()
            
            # Apply filters based on user input
            # Partial search with wildcard support (case-insensitive)
            if recipe_name:
                qs = qs.filter(name__icontains=recipe_name)
            
            # Filter by difficulty if selected
            if difficulty:
                # Filter recipes by calculating difficulty on the fly
                filtered_recipes = []
                for recipe in qs:
                    if recipe.difficulty() == difficulty:
                        filtered_recipes.append(recipe.id)
                qs = qs.filter(id__in=filtered_recipes)
            
            # If recipes found, convert to DataFrame
            if qs.exists():
                # Convert QuerySet to DataFrame
                recipes_df = pd.DataFrame(qs.values())
                
                # Add computed fields
                recipes_df['difficulty'] = [recipe.difficulty() for recipe in qs]
                recipes_df['ingredients_count'] = [len(recipe.ingredients_list()) for recipe in qs]
                
                # Generate chart
                chart = get_chart(chart_type, recipes_df, labels=recipes_df['name'].values)
                
                # Convert DataFrame to HTML for display
                recipes_df = recipes_df.to_html(
                    classes='table table-striped',
                    index=False,
                    columns=['name', 'cooking_time', 'difficulty', 'ingredients_count', 'category'],
                    escape=False
                )
        
        # Add to context
        context['recipes_df'] = recipes_df
        context['chart'] = chart
        
        return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
    """Protected detail view for a single recipe, including computed difficulty."""
    model = Recipe
    template_name = 'recipe/recipe_detail.html'

