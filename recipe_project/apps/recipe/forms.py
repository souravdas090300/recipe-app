"""
Recipe App Forms Module

This module defines forms used in the Recipe application for searching,
filtering, and data visualization.

Forms:
    RecipeSearchForm: Search and filter recipes with chart visualization options

Constants:
    CHART_CHOICES: Available chart types for data visualization
    DIFFICULTY_CHOICES: Recipe difficulty levels for filtering
"""

from django import forms

# Chart type choices for data visualization
# Format: (value, display_label)
# These values map to chart generation logic in utils.py
CHART_CHOICES = (
    ('#1', 'Bar chart'),   # Vertical bar chart showing cooking times
    ('#2', 'Pie chart'),   # Pie chart showing recipe distribution
    ('#3', 'Line chart')   # Line chart showing trends across recipes
)

# Difficulty filter choices
# Format: (value, display_label)
# Empty string ('') represents "All" - no filter applied
# Other values match the return values from Recipe.difficulty() method
DIFFICULTY_CHOICES = (
    ('', 'All'),                      # Show all recipes (no filter)
    ('Easy', 'Easy'),                 # < 10 min, < 4 ingredients
    ('Medium', 'Medium'),             # < 10 min, >= 4 ingredients
    ('Intermediate', 'Intermediate'), # >= 10 min, < 4 ingredients
    ('Hard', 'Hard')                  # >= 10 min, >= 4 ingredients
)


class RecipeSearchForm(forms.Form):
    """
    Form for searching and filtering recipes with chart visualization.
    
    This form allows users to:
    - Search recipes by name (partial match, case-insensitive)
    - Filter recipes by ingredient (searches in ingredients text)
    - Filter recipes by difficulty level
    - Select chart type for data visualization
    
    All fields are optional except chart_type, allowing flexible searches.
    The form supports both POST (form submission) and GET (URL parameters).
    
    Fields:
        recipe_name: Text input for recipe name search
        ingredient: Text input for ingredient search
        chart_type: Dropdown for selecting visualization chart
        difficulty: Dropdown for filtering by difficulty level
    
    Example Usage:
        >>> form = RecipeSearchForm(request.POST)
        >>> if form.is_valid():
        ...     recipe_name = form.cleaned_data['recipe_name']
        ...     chart_type = form.cleaned_data['chart_type']
    """
    
    # Recipe name search field
    # max_length=120: Matches Recipe.name max length
    # required=False: Field is optional (allows showing all recipes)
    # widget: Customizes HTML rendering with placeholder and CSS class
    recipe_name = forms.CharField(
        max_length=120, 
        required=False,  # Optional: empty value shows all recipes
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter recipe name (leave blank for all recipes)',
            'class': 'search-input'  # CSS class for styling
        })
    )
    
    # Ingredient search field
    # Searches for ingredient name within the comma-separated ingredients text
    # max_length=120: Reasonable limit for ingredient name
    # required=False: Field is optional (no ingredient filter if empty)
    ingredient = forms.CharField(
        max_length=120,
        required=False,  # Optional: empty value shows all recipes
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by ingredient (e.g., chicken)',
            'class': 'search-input'  # CSS class for styling
        })
    )
    
    # Chart type selection field
    # ChoiceField: Dropdown select element
    # choices=CHART_CHOICES: Limits options to predefined chart types
    # Required field (no required=False) - user must select a chart type
    # Values: '#1' (bar), '#2' (pie), '#3' (line)
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,  # Dropdown options from CHART_CHOICES constant
        widget=forms.Select(attrs={
            'class': 'chart-select'  # CSS class for styling
        })
    )
    
    # Difficulty filter field
    # ChoiceField: Dropdown select element
    # choices=DIFFICULTY_CHOICES: Limits options to difficulty levels + "All"
    # required=False: Field is optional (empty/All shows recipes of all difficulties)
    # Default is '' (All) which doesn't apply any difficulty filter
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,  # Dropdown options from DIFFICULTY_CHOICES constant
        required=False,  # Optional: empty value shows all difficulties
        widget=forms.Select(attrs={
            'class': 'difficulty-select'  # CSS class for styling
        })
    )
