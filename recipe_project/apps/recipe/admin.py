"""
Recipe App Admin Configuration Module

This module configures the Django admin interface for the Recipe application.
It customizes the admin panel appearance and defines how Recipe models
are displayed and managed in the admin interface.

Admin Classes:
    RecipeAdmin: Customizes Recipe model admin interface
"""

from django.contrib import admin
from .models import Recipe


# Customize admin site headers
# These appear in browser title and admin panel header

# Main header displayed at top of admin pages
admin.site.site_header = "Recipe App Administration"

# Browser tab title for admin pages
admin.site.site_title = "Recipe App Admin"

# Welcome message on admin index page
admin.site.index_title = "Welcome to Recipe App Admin Panel"


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for Recipe model.
    
    This class customizes how recipes are displayed and managed in the
    Django admin panel. It provides search, filtering, and display options
    for efficient recipe management.
    
    Features:
    - List view with key recipe information
    - Search by name, ingredients, and description
    - Filter by user and cooking time
    - Display calculated difficulty level
    
    Attributes:
        list_display: Columns shown in recipe list view
        list_filter: Sidebar filters for narrowing recipe list
        search_fields: Fields searchable via admin search box
    
    Methods:
        get_difficulty: Display calculated difficulty in list view
    """
    
    # Columns to display in the recipe list view (admin changelist)
    # Tuple of field names and method names
    # Users see: Name | Cooking Time | Owner | Difficulty
    list_display = ('name', 'cooking_time', 'user', 'get_difficulty')
    
    # Sidebar filters for narrowing down recipe list
    # Creates filter options in right sidebar
    # - user: Dropdown of all users who created recipes
    # - cooking_time: Range filters for cooking time values
    list_filter = ('user', 'cooking_time')
    
    # Fields that can be searched using the admin search box
    # Searches are case-insensitive and use partial matching
    # Search box appears at top of recipe list
    # - name: Search in recipe names
    # - ingredients: Search in ingredient lists
    # - description: Search in recipe descriptions
    search_fields = ('name', 'ingredients', 'description')
    
    def get_difficulty(self, obj):
        """
        Display calculated difficulty level in admin list view.
        
        This method is called for each recipe in the list view to display
        its difficulty level. Since difficulty is a computed property
        (not a database field), we need this custom method.
        
        Args:
            obj (Recipe): Recipe instance being displayed
        
        Returns:
            str: Difficulty level ('Easy', 'Medium', 'Intermediate', or 'Hard')
        
        Example:
            Recipe with 5 min cooking time and 2 ingredients -> 'Easy'
        """
        # Call the difficulty() method on the Recipe instance
        return obj.difficulty()
    
    # Set the column header for this custom method
    # This appears in the list view table header
    get_difficulty.short_description = 'Difficulty'

