from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.recipe.models import Recipe
import random

CATEGORIES = ['breakfast','lunch','dinner','dessert','snack']

SAMPLE_RECIPES = [
    ("Classic Pancakes", 15, "flour, milk, egg, sugar, baking powder, butter", "breakfast"),
    ("Veggie Omelette", 10, "egg, bell pepper, onion, tomato, cheese", "breakfast"),
    ("Grilled Chicken", 30, "chicken, olive oil, garlic, lemon, pepper, salt", "dinner"),
    ("Tomato Pasta", 25, "pasta, tomato, garlic, basil, olive oil, parmesan", "lunch"),
    ("Beef Stir Fry", 20, "beef, soy sauce, broccoli, carrot, garlic, ginger", "dinner"),
    ("Fruit Salad", 8, "apple, banana, orange, grapes, honey, mint", "snack"),
    ("Avocado Toast", 7, "bread, avocado, lemon, chili flakes, salt", "breakfast"),
    ("Chocolate Brownies", 40, "flour, cocoa, sugar, egg, butter, chocolate", "dessert"),
    ("Caesar Salad", 12, "lettuce, croutons, parmesan, chicken, caesar dressing", "lunch"),
    ("Fish Tacos", 25, "fish, tortilla, cabbage, lime, salsa, avocado", "dinner"),
    ("Lentil Soup", 35, "lentils, carrot, onion, celery, garlic, cumin", "lunch"),
    ("Banana Smoothie", 5, "banana, milk, honey, ice", "snack"),
    ("Margarita Pizza", 18, "pizza dough, tomato, mozzarella, basil, olive oil", "dinner"),
    ("Chicken Biryani", 60, "rice, chicken, yogurt, onion, spices, saffron", "dinner"),
    ("Veggie Sandwich", 10, "bread, cucumber, tomato, lettuce, mayo, cheese", "lunch"),
]

class Command(BaseCommand):
    help = "Load 15+ sample recipes for demo purposes"

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='demo')

    def handle(self, *args, **options):
        username = options['username']
        User = get_user_model()
        user, _ = User.objects.get_or_create(username=username)
        if not user.password:
            user.set_password('demo')
            user.save()

        created = 0
        for name, time, ingredients, category in SAMPLE_RECIPES:
            obj, was_created = Recipe.objects.get_or_create(
                name=name,
                defaults={
                    'cooking_time': time,
                    'ingredients': ingredients,
                    'description': f"Delicious {name} recipe. Easy to make and perfect for any occasion!",
                    'category': category,
                    'user': user,
                }
            )
            if was_created:
                created += 1
        self.stdout.write(self.style.SUCCESS(f"Sample recipes load complete. Created: {created}"))
