import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from apps.recipe.models import Recipe

recipes = Recipe.objects.all()
print(f'Total recipes in database: {recipes.count()}')
print('\nRecipe list:')
for r in recipes:
    print(f'- {r.name} (Image: {r.pic.name if r.pic else "None"})')
