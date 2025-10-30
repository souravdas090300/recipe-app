from django import forms

# Chart type choices for data visualization
CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart')
)

# Difficulty filter choices
DIFFICULTY_CHOICES = (
    ('', 'All'),
    ('Easy', 'Easy'),
    ('Medium', 'Medium'),
    ('Intermediate', 'Intermediate'),
    ('Hard', 'Hard')
)


class RecipeSearchForm(forms.Form):
    """Form for searching recipes and selecting chart type for visualization."""
    recipe_name = forms.CharField(
        max_length=120, 
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter recipe name (leave blank for all recipes)',
            'class': 'search-input'
        })
    )
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        widget=forms.Select(attrs={'class': 'chart-select'})
    )
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'difficulty-select'})
    )
