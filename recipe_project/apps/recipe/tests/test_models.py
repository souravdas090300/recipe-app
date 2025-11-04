from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.recipe.models import Recipe


User = get_user_model()


class RecipeModelTests(TestCase):
    """Test cases for the Recipe model."""

    def setUp(self):
        """Set up test user and recipe."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            cooking_time=5,
            ingredients='salt, water, sugar',
            description='Test description',
            user=self.user
        )

    def test_recipe_creation(self):
        """Test recipe is created successfully."""
        self.assertEqual(self.recipe.name, 'Test Recipe')
        self.assertEqual(self.recipe.cooking_time, 5)
        self.assertEqual(self.recipe.ingredients, 'salt, water, sugar')
        self.assertEqual(self.recipe.user, self.user)

    def test_recipe_str_method(self):
        """Test the string representation of recipe."""
        self.assertEqual(str(self.recipe), 'Test Recipe')

    def test_ingredients_list_method(self):
        """Test ingredients_list helper method."""
        expected = ['salt', 'water', 'sugar']
        self.assertEqual(self.recipe.ingredients_list(), expected)

    def test_ingredients_list_empty(self):
        """Test ingredients_list with empty ingredients."""
        recipe = Recipe.objects.create(
            name='Empty Recipe',
            cooking_time=10,
            ingredients='',
            user=self.user
        )
        self.assertEqual(recipe.ingredients_list(), [])

    def test_difficulty_easy(self):
        """Test difficulty calculation for Easy recipe."""
        # cooking_time < 10 and ingredients < 4
        recipe = Recipe.objects.create(
            name='Easy Recipe',
            cooking_time=5,
            ingredients='salt, water',
            user=self.user
        )
        self.assertEqual(recipe.difficulty(), 'Easy')

    def test_difficulty_medium(self):
        """Test difficulty calculation for Medium recipe."""
        # cooking_time < 10 and ingredients >= 4
        recipe = Recipe.objects.create(
            name='Medium Recipe',
            cooking_time=8,
            ingredients='salt, water, sugar, flour',
            user=self.user
        )
        self.assertEqual(recipe.difficulty(), 'Medium')

    def test_difficulty_intermediate(self):
        """Test difficulty calculation for Intermediate recipe."""
        # cooking_time >= 10 and ingredients < 4
        recipe = Recipe.objects.create(
            name='Intermediate Recipe',
            cooking_time=15,
            ingredients='chicken, salt',
            user=self.user
        )
        self.assertEqual(recipe.difficulty(), 'Intermediate')

    def test_difficulty_hard(self):
        """Test difficulty calculation for Hard recipe."""
        # cooking_time >= 10 and ingredients >= 4
        recipe = Recipe.objects.create(
            name='Hard Recipe',
            cooking_time=30,
            ingredients='chicken, beef, pork, fish, vegetables',
            user=self.user
        )
        self.assertEqual(recipe.difficulty(), 'Hard')

    def test_description_null_allowed(self):
        """Test that description can be null."""
        recipe = Recipe.objects.create(
            name='No Description Recipe',
            cooking_time=10,
            ingredients='salt, pepper',
            description=None,
            user=self.user
        )
        self.assertIsNone(recipe.description)

    def test_user_relationship(self):
        """Test ForeignKey relationship with User."""
        self.assertEqual(self.recipe.user, self.user)
        # Verify reverse relationship (one user can have many recipes)
        self.assertIn(self.recipe, self.user.recipes.all())
