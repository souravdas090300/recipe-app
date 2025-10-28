from django.db import models


class Recipe(models.Model):
	"""Simple Recipe model using a comma-separated ingredients string.

	Mentor guidance: keep a single app (recipes) and store ingredients as a
	comma-separated string (e.g., "salt, water, sugar").
	"""

	name = models.CharField(max_length=120)
	cooking_time = models.PositiveIntegerField(help_text='in minutes')
	# Store ingredients as a comma-separated string (TextField)
	ingredients = models.TextField(help_text='Comma-separated list of ingredients')
	description = models.TextField(blank=True, null=True)
	pic = models.ImageField(upload_to='recipes', default='no_picture.jpg')
	# ForeignKey relationship with User for recipe ownership (one user can have many recipes)
	user = models.ForeignKey("auth.User", on_delete=models.CASCADE, related_name='recipes')

	def __str__(self) -> str:
		return self.name

	# Helper methods (not stored in DB)
	def ingredients_list(self) -> list[str]:
		"""Return ingredients as a normalized list of strings from CSV."""
		if not self.ingredients:
			return []
		return [item.strip() for item in self.ingredients.split(',') if item.strip()]

	def difficulty(self) -> str:
		"""Compute difficulty based on cooking time and number of ingredients.

		Easy: cooking_time < 10 and ingredients < 4
		Medium: cooking_time < 10 and ingredients >= 4
		Intermediate: cooking_time >= 10 and ingredients < 4
		Hard: otherwise
		"""
		num_ingredients = len(self.ingredients_list())
		if self.cooking_time < 10 and num_ingredients < 4:
			return 'Easy'
		if self.cooking_time < 10 and num_ingredients >= 4:
			return 'Medium'
		if self.cooking_time >= 10 and num_ingredients < 4:
			return 'Intermediate'
		return 'Hard'
