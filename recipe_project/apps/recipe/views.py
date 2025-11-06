"""
Recipe App Views Module

This module contains all view classes and functions for the Recipe application.
It handles displaying recipes, search functionality, and creating new recipes.

Views:
    - home: Homepage view (public access)
    - about: About page view (public access)
    - RecipeListView: List all recipes with search/filter (login required)
    - RecipeDetailView: Display single recipe details (login required)
    - RecipeCreateView: Form to create new recipes (login required)
"""

from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import Recipe
# LoginRequiredMixin: Mixin to protect class-based views - requires user authentication
from django.contrib.auth.mixins import LoginRequiredMixin
# RecipeSearchForm: Custom form for searching and filtering recipes
from .forms import RecipeSearchForm
# pandas: Library for data manipulation and analysis (used for charts)
import pandas as pd
# get_chart: Utility function to generate data visualization charts
from .utils import get_chart

# Create your views here.

def home(request):
    """
    Homepage view for the Recipe App.
    
    This is the landing page that welcomes users and provides navigation
    to login, signup, or browse recipes. No authentication required.
    
    Args:
        request: HttpRequest object containing metadata about the request
    
    Returns:
        HttpResponse: Rendered homepage template
    
    Template:
        recipe/recipes_home.html
    """
    return render(request, 'recipe/recipes_home.html')


def about(request):
    """
    About page view displaying developer information.
    
    Shows information about the developer, project description,
    and links to GitHub and LinkedIn profiles. No authentication required.
    
    Args:
        request: HttpRequest object containing metadata about the request
    
    Returns:
        HttpResponse: Rendered about page template
    
    Template:
        recipe/about.html
    """
    return render(request, 'recipe/about.html')


class RecipeListView(LoginRequiredMixin, ListView):
    """
    Display a list of all recipes with search and filter capabilities.
    
    This view is protected by LoginRequiredMixin, requiring users to be
    authenticated before accessing the recipe list. It supports:
    - Searching by recipe name (partial match, case-insensitive)
    - Filtering by ingredient (partial match in ingredients list)
    - Filtering by difficulty level (Easy, Medium, Intermediate, Hard)
    - Data visualization with charts (Bar, Pie, Line)
    - Pagination (12 recipes per page)
    
    Attributes:
        model: Recipe model class
        template_name: Path to the template file
        paginate_by: Number of recipes per page (12)
    
    Methods:
        post: Handles POST requests for search form submission
        get_context_data: Adds search results and charts to template context
    
    Template:
        recipe/recipes_list.html
    
    Context Variables:
        - object_list: QuerySet of Recipe objects (paginated)
        - form: RecipeSearchForm instance
        - recipes_df: DataFrame converted to HTML table (if search performed)
        - chart: Base64 encoded chart image (if chart type selected)
        - querystring: URL parameters for pagination links
    """
    model = Recipe
    template_name = 'recipe/recipes_list.html'
    paginate_by = 12  # Show 12 recipes per page
    
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for search form submission.
        
        When users submit the search form via POST, this method redirects
        the handling to the GET method to process the search criteria.
        
        Args:
            request: HttpRequest object with POST data
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments
        
        Returns:
            HttpResponse: Result from get() method with search results
        """
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        Add search form, filtered results, and charts to template context.
        
        This method processes search criteria from either POST (form submission)
        or GET (URL parameters) requests, filters recipes accordingly, and
        generates data visualizations.
        
        Processing Steps:
        1. Get parent context (includes paginated recipe list)
        2. Determine request method (POST for form, GET for URL params)
        3. Initialize and validate RecipeSearchForm
        4. Apply search filters:
           - recipe_name: Case-insensitive partial match on name field
           - ingredient: Case-insensitive search in ingredients text
           - difficulty: Calculated difficulty level filter
        5. Convert filtered results to pandas DataFrame
        6. Generate chart visualization based on selected chart type
        7. Build querystring for pagination links
        
        Args:
            **kwargs: Arbitrary keyword arguments from parent class
        
        Returns:
            dict: Context dictionary with additional keys:
                - form: RecipeSearchForm instance
                - recipes_df: HTML table of search results (or None)
                - chart: Base64 encoded chart image (or None)
                - querystring: URL parameters for pagination
        """
        # Get the base context from parent class (includes object_list, paginator, etc.)
        context = super().get_context_data(**kwargs)
        
        # Support both POST (form submit) and GET (homepage search/navigation)
        # POST: User submitted search form
        # GET: User clicked link with search parameters or navigated from homepage
        if self.request.method == 'POST':
            data = self.request.POST
        elif self.request.method == 'GET':
            data = self.request.GET
        else:
            data = None

        # Create an instance of RecipeSearchForm with the request data
        # If no data, form will be empty (initial state)
        form = RecipeSearchForm(data or None)
        context['form'] = form
        
        # Initialize variables for search results and chart
        recipes_df = None  # Will hold DataFrame of results
        chart = None       # Will hold base64 encoded chart image
        
        # Check if form was submitted and is valid
        if self.request.method in ['POST', 'GET'] and form.is_valid():
            # Extract search criteria from cleaned form data
            recipe_name = data.get('recipe_name')      # Partial name search
            ingredient = data.get('ingredient')         # Ingredient filter
            chart_type = data.get('chart_type')        # Chart visualization type (#1, #2, #3)
            difficulty = data.get('difficulty')         # Difficulty level filter
            category = data.get('category')             # Category filter (breakfast, lunch, dinner, dessert, snack)
            
            # Start with all recipes in the database
            qs = Recipe.objects.all()
            
            # Apply filters based on user input
            # Filter 1: Recipe name - Partial search with wildcard support (case-insensitive)
            # Example: "pasta" matches "Spaghetti Pasta", "Pasta Primavera", etc.
            if recipe_name:
                qs = qs.filter(name__icontains=recipe_name)
            
            # Filter 2: Ingredient - Substring search (case-insensitive) against CSV TextField
            # Example: "tomato" matches recipes with "tomato, onion, garlic"
            if ingredient:
                qs = qs.filter(ingredients__icontains=ingredient)
            
            # Filter 3: Category - Exact match filter for recipe category
            # Example: "breakfast" shows only breakfast recipes
            if category:
                qs = qs.filter(category=category)
            
            # Filter 4: Difficulty - Filter by calculated difficulty level
            # Note: difficulty() is a method, not a database field, so we filter manually
            if difficulty:
                # Create list to store IDs of recipes matching difficulty
                filtered_recipes = []
                for recipe in qs:
                    # Call difficulty() method on each recipe instance
                    if recipe.difficulty() == difficulty:
                        filtered_recipes.append(recipe.id)
                # Filter queryset to only include matching recipe IDs
                qs = qs.filter(id__in=filtered_recipes)
            
            # If recipes found after filtering, prepare data for display
            if qs.exists():
                # Convert Django QuerySet to pandas DataFrame for data analysis
                # .values() returns dict-like objects with database fields
                recipes_df = pd.DataFrame(qs.values())
                
                # Add computed fields not stored in database
                # Calculate difficulty for each recipe (Easy, Medium, Intermediate, Hard)
                recipes_df['difficulty'] = [recipe.difficulty() for recipe in qs]
                # Count ingredients in each recipe (used for analysis)
                recipes_df['ingredients_count'] = [len(recipe.ingredients_list()) for recipe in qs]
                
                # Generate chart visualization if chart type selected
                # chart_type: '#1' = Bar, '#2' = Pie, '#3' = Line
                # Returns base64 encoded image string for embedding in HTML
                chart = get_chart(chart_type, recipes_df, labels=recipes_df['name'].values)
                
                # Convert DataFrame to HTML table for display in template
                # classes: Bootstrap CSS classes for styling
                # index: Don't show DataFrame index column
                # columns: Select which columns to display
                # escape: Don't escape HTML characters
                recipes_df = recipes_df.to_html(
                    classes='table table-striped',
                    index=False,
                    columns=['name', 'cooking_time', 'difficulty', 'ingredients_count', 'category'],
                    escape=False
                )
        
        # Build querystring (exclude 'page') to preserve filters in pagination links
        # When user clicks next/previous page, we want to keep their search criteria
        # Copy request parameters (GET for links, POST for form submission)
        params = self.request.GET.copy() if self.request.method == 'GET' else self.request.POST.copy()
        # Remove 'page' parameter if it exists (pagination will add it back)
        if 'page' in params:
            params.pop('page')
        # Convert parameters to URL encoded string
        querystring = params.urlencode()
        # Add '&' prefix if there are parameters (for appending to pagination URLs)
        context['querystring'] = ('&' + querystring) if querystring else ''

        # Add search results and chart to context
        context['recipes_df'] = recipes_df  # HTML table or None
        context['chart'] = chart            # Base64 image or None
        
        return context


class RecipeDetailView(LoginRequiredMixin, DetailView):
    """
    Display detailed information for a single recipe.
    
    This view is protected by LoginRequiredMixin, requiring users to be
    authenticated before viewing recipe details. It shows:
    - Recipe name, cooking time, category
    - Complete ingredient list (parsed from CSV string)
    - Recipe description/instructions
    - Recipe image (if available)
    - Calculated difficulty level
    
    Attributes:
        model: Recipe model class
        template_name: Path to the template file
    
    Template:
        recipe/recipe_detail.html
    
    Context Variables:
        - object: Recipe instance (also available as 'recipe')
    
    URL Pattern:
        /recipes/<int:pk>/ where pk is the recipe's primary key
    """
    model = Recipe
    template_name = 'recipe/recipe_detail.html'

class RecipeCreateView(LoginRequiredMixin, CreateView):
    """
    Form view for creating new recipes.
    
    This view is protected by LoginRequiredMixin, allowing only authenticated
    users to add new recipes. Automatically assigns the current user as the
    recipe owner.
    
    Features:
    - All recipe fields available for input
    - Image upload support (optional)
    - Automatic user assignment (recipe owner)
    - Form validation (required fields, data types)
    - Redirects to recipe list after successful creation
    
    Attributes:
        model: Recipe model class
        fields: List of fields to include in the form
        template_name: Path to the template file
    
    Methods:
        form_valid: Called when form validates successfully, sets recipe owner
        get_success_url: Returns URL to redirect to after creation
    
    Template:
        recipe/recipe_form.html
    
    Form Fields:
        - name: Recipe name (required)
        - cooking_time: Time in minutes (required, positive integer)
        - ingredients: Comma-separated ingredient list (required)
        - description: Recipe instructions (optional)
        - category: Recipe category dropdown (optional)
        - pic: Recipe image upload (optional)
    """
    model = Recipe
    fields = ['name', 'cooking_time', 'ingredients', 'description', 'category', 'pic']
    template_name = 'recipe/recipe_form.html'

    def form_valid(self, form):
        """
        Process valid form submission.
        
        Automatically assigns the currently logged-in user as the recipe owner
        before saving the recipe to the database.
        
        Args:
            form: Validated ModelForm instance with cleaned data
        
        Returns:
            HttpResponseRedirect: Redirect to success URL (recipe list)
        """
        # Set the owner to current user (accessed via self.request.user)
        form.instance.user = self.request.user
        # Call parent's form_valid to save the form and redirect
        return super().form_valid(form)

    def get_success_url(self):
        """
        Determine where to redirect after successful recipe creation.
        
        Returns:
            str: URL path to the recipe list view
        """
        # Redirect to recipes list after creation
        from django.urls import reverse
        return reverse('recipe:recipes-list')

