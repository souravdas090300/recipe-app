"""
Recipe App URL Configuration

This module defines URL patterns for the Recipe application.
It maps URL paths to their corresponding view functions and classes.

URL Patterns:
    / - Homepage (public)
    /about/ - About page (public)
    /recipes/ - Recipe list with search (login required)
    /recipes/add/ - Add new recipe form (login required)
    /recipes/<id>/ - Recipe detail page (login required)

Namespace:
    app_name='recipe' allows reverse URL lookups like 'recipe:home'
"""

from django.urls import path
from . import views

# Application namespace for URL reversing
# Allows us to use 'recipe:home', 'recipe:recipes-list', etc.
# in templates and views ({% url 'recipe:home' %})
app_name = 'recipe'

urlpatterns = [
    # Homepage URL
    # Pattern: '' (root path within app)
    # View: home function view
    # Name: 'home' (accessible as 'recipe:home')
    # Example URL: http://example.com/
    # Access: Public (no login required)
    path('', views.home, name='home'),
    
    # About page URL
    # Pattern: 'about/'
    # View: about function view
    # Name: 'about' (accessible as 'recipe:about')
    # Example URL: http://example.com/about/
    # Access: Public (no login required)
    path('about/', views.about, name='about'),
    
    # Recipe list view with search and filtering
    # Pattern: 'recipes/'
    # View: RecipeListView class-based view
    # Name: 'recipes-list' (accessible as 'recipe:recipes-list')
    # Example URL: http://example.com/recipes/
    # Access: Login required (LoginRequiredMixin)
    # Features: Search, filter by difficulty/ingredient, data visualization
    path('recipes/', views.RecipeListView.as_view(), name='recipes-list'),
    
    # Add new recipe form
    # Pattern: 'recipes/add/'
    # View: RecipeCreateView class-based view
    # Name: 'recipe-add' (accessible as 'recipe:recipe-add')
    # Example URL: http://example.com/recipes/add/
    # Access: Login required (LoginRequiredMixin)
    # Note: Placed BEFORE <int:pk> pattern to avoid conflict
    path('recipes/add/', views.RecipeCreateView.as_view(), name='recipe-add'),
    
    # Recipe detail view
    # Pattern: 'recipes/<int:pk>/'
    # View: RecipeDetailView class-based view
    # Name: 'recipe-detail' (accessible as 'recipe:recipe-detail')
    # Example URL: http://example.com/recipes/5/
    # Access: Login required (LoginRequiredMixin)
    # URL Parameter: pk (primary key) - recipe ID as integer
    # Note: Must come AFTER 'add/' pattern to avoid capturing 'add' as pk
    path('recipes/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe-detail'),
]
