"""
Recipe App Models Module

This module defines the database models for the Recipe application.
It contains the Recipe model which stores all recipe information including
name, cooking time, ingredients, and user relationships.

Models:
    Recipe: Main model for storing recipe data
"""

from django.db import models
from django.urls import reverse


class Recipe(models.Model):
	"""
	Recipe model for storing recipe information.
	
	This model stores all data related to a recipe including its name,
	cooking time, ingredients (as comma-separated values), description,
	category, image, and the user who created it.
	
	The model follows mentor guidance to:
	- Keep a single app (recipes)
	- Store ingredients as comma-separated string (not a separate model)
	- Use Django's built-in User model for ownership
	
	Attributes:
		name (CharField): Recipe name, max 120 characters
		cooking_time (PositiveIntegerField): Cooking time in minutes (must be > 0)
		ingredients (TextField): Comma-separated list of ingredients
		description (TextField): Recipe instructions/description (optional)
		category (CharField): Recipe category from predefined choices
		pic (ImageField): Recipe image, stored in media/recipes/ (optional)
		user (ForeignKey): Reference to User model (recipe owner)
	
	Methods:
		__str__(): Returns recipe name as string representation
		ingredients_list(): Converts CSV ingredients to Python list
		difficulty(): Calculates difficulty based on time and ingredient count
		get_absolute_url(): Returns URL for recipe detail page
	
	Example:
		>>> recipe = Recipe.objects.create(
		...     name="Pasta",
		...     cooking_time=15,
		...     ingredients="pasta, tomato, garlic, olive oil",
		...     user=user_instance
		... )
		>>> recipe.difficulty()
		'Intermediate'
		>>> recipe.ingredients_list()
		['pasta', 'tomato', 'garlic', 'olive oil']
	"""

	# Category choices for recipe classification
	# Format: (database_value, human_readable_label)
	CATEGORY_CHOICES = [
		('breakfast', 'Breakfast'),  # Morning meals
		('lunch', 'Lunch'),          # Midday meals
		('dinner', 'Dinner'),        # Evening meals
		('dessert', 'Dessert'),      # Sweet dishes
		('snack', 'Snack'),          # Light meals/snacks
	]

	# Recipe name field
	# max_length=120: Limits recipe name to 120 characters
	# This is the primary identifier for the recipe
	name = models.CharField(max_length=120)
	
	# Cooking time in minutes
	# PositiveIntegerField: Only allows positive integers (>= 0)
	# help_text: Provides guidance in admin and forms
	cooking_time = models.PositiveIntegerField(help_text='in minutes')
	
	# Ingredients stored as comma-separated values (CSV)
	# TextField: Allows longer text than CharField (no character limit)
	# Format: "ingredient1, ingredient2, ingredient3"
	# Example: "salt, water, sugar, flour"
	ingredients = models.TextField(help_text='Comma-separated list of ingredients')
	
	# Recipe description/instructions (optional)
	# TextField: For longer text content
	# blank=True: Field not required in forms
	# null=True: Allows NULL in database
	description = models.TextField(blank=True, null=True)
	
	# Recipe category (breakfast, lunch, dinner, dessert, snack)
	# max_length=20: Maximum length for category value
	# choices=CATEGORY_CHOICES: Limits values to predefined list
	# default='lunch': Default value if not specified
	category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='lunch')
	
	# Recipe image field
	# ImageField: Special field for image files (requires Pillow library)
	# upload_to='recipes': Images stored in MEDIA_ROOT/recipes/ directory
	# blank=True, null=True: Image is optional (not required)
	# Note: Changed from default='no_picture.jpg' to avoid missing file errors on Heroku
	pic = models.ImageField(upload_to='recipes', blank=True, null=True)
	
	# Foreign key relationship to Django's built-in User model
	# "auth.User": String reference to avoid circular imports
	# on_delete=models.CASCADE: When user is deleted, delete their recipes too
	# related_name='recipes': Allows user.recipes.all() to get all user's recipes
	# This creates a one-to-many relationship (one user can have many recipes)
	user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='recipes')

	def __str__(self) -> str:
		"""
		String representation of Recipe instance.
		
		Returns the recipe name when the object is converted to string.
		Used in Django admin, shell, and templates.
		
		Returns:
			str: Recipe name
		
		Example:
			>>> recipe = Recipe.objects.get(id=1)
			>>> print(recipe)
			'Spaghetti Carbonara'
		"""
		return self.name

	# Helper methods (computed fields not stored in database)
	
	def ingredients_list(self) -> list[str]:
		"""
		Convert comma-separated ingredients string to a list.
		
		Parses the ingredients TextField and returns a normalized list
		of ingredient names with whitespace stripped.
		
		Process:
		1. Split ingredients string by comma delimiter
		2. Strip whitespace from each ingredient
		3. Filter out empty strings
		4. Return as Python list
		
		Returns:
			list[str]: List of ingredient names (empty list if no ingredients)
		
		Example:
			>>> recipe.ingredients = "salt, water, sugar"
			>>> recipe.ingredients_list()
			['salt', 'water', 'sugar']
			
			>>> recipe.ingredients = "  tomato  ,  onion  ,  garlic  "
			>>> recipe.ingredients_list()
			['tomato', 'onion', 'garlic']
			
			>>> recipe.ingredients = ""
			>>> recipe.ingredients_list()
			[]
		"""
		# Return empty list if ingredients field is empty
		if not self.ingredients:
			return []
		# Split by comma, strip whitespace, filter empty strings
		return [item.strip() for item in self.ingredients.split(',') if item.strip()]

	def difficulty(self) -> str:
		"""
		Calculate recipe difficulty based on cooking time and ingredient count.
		
		Difficulty Levels:
		- Easy: cooking_time < 10 AND ingredients < 4
		  (Quick recipes with few ingredients)
		
		- Medium: cooking_time < 10 AND ingredients >= 4
		  (Quick recipes with many ingredients)
		
		- Intermediate: cooking_time >= 10 AND ingredients < 4
		  (Longer recipes with few ingredients)
		
		- Hard: cooking_time >= 10 AND ingredients >= 4
		  (Longer recipes with many ingredients)
		
		Returns:
			str: One of 'Easy', 'Medium', 'Intermediate', or 'Hard'
		
		Example:
			>>> recipe.cooking_time = 5
			>>> recipe.ingredients = "salt, water"  # 2 ingredients
			>>> recipe.difficulty()
			'Easy'
			
			>>> recipe.cooking_time = 15
			>>> recipe.ingredients = "pasta, tomato, garlic, oil, cheese"  # 5 ingredients
			>>> recipe.difficulty()
			'Hard'
		"""
		# Get number of ingredients by counting items in list
		num_ingredients = len(self.ingredients_list())
		
		# Easy: Quick to cook (< 10 min) with few ingredients (< 4)
		if self.cooking_time < 10 and num_ingredients < 4:
			return 'Easy'
		
		# Medium: Quick to cook (< 10 min) but many ingredients (>= 4)
		if self.cooking_time < 10 and num_ingredients >= 4:
			return 'Medium'
		
		# Intermediate: Takes time (>= 10 min) but few ingredients (< 4)
		if self.cooking_time >= 10 and num_ingredients < 4:
			return 'Intermediate'
		
		# Hard: Takes time (>= 10 min) and many ingredients (>= 4)
		return 'Hard'

	def get_absolute_url(self) -> str:
		"""
		Get the canonical URL for this recipe's detail page.
		
		Uses Django's reverse URL resolution to generate the URL path
		for viewing this recipe's details.
		
		Returns:
			str: URL path to recipe detail view (e.g., '/recipes/5/')
		
		Example:
			>>> recipe.id = 5
			>>> recipe.get_absolute_url()
			'/recipes/5/'
		
		Notes:
			- Used by Django's get_absolute_url() convention
			- Allows {{ recipe.get_absolute_url }} in templates
			- 'recipe:recipe-detail' references the named URL pattern
			- kwargs={'pk': self.pk} passes the recipe's primary key
		"""
		return reverse('recipe:recipe-detail', kwargs={'pk': self.pk})
