from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.recipe.models import Recipe


User = get_user_model()


class RecipeViewsTests(TestCase):
    """Test cases for recipe views."""

    def test_home_view_status_code(self):
        """Test home view returns 200 status code."""
        response = self.client.get(reverse('recipe:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        """Test home view uses correct template."""
        response = self.client.get(reverse('recipe:home'))
        self.assertTemplateUsed(response, 'recipe/recipes_home.html')


class AdminTests(TestCase):
    """Test cases for Django admin functionality."""

    def setUp(self):
        """Set up test user and recipe for admin tests."""
        # Create a superuser for admin access
        self.admin_username = 'admin_test'
        self.admin_password = 'StrongPass123!'
        self.admin = User.objects.create_superuser(
            username=self.admin_username,
            email='admin_test@example.com',
            password=self.admin_password,
        )

        # Create a regular user for recipe ownership
        self.user = User.objects.create_user(
            username='recipeowner',
            email='owner@example.com',
            password='pass123'
        )

        # Create a sample recipe with CSV ingredients
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            cooking_time=5,
            ingredients='salt, water, sugar',
            description='Test description',
            user=self.user
        )

    def test_admin_requires_login(self):
        """Test admin requires authentication."""
        # Accessing admin without login should redirect to login page
        response = self.client.get('/admin/', follow=False)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

    def test_admin_recipe_changelist_shows_difficulty(self):
        """Test admin changelist displays difficulty column."""
        # Login to admin
        self.client.login(username=self.admin_username, password=self.admin_password)

        # Access Recipe changelist
        response = self.client.get('/admin/recipe/recipe/')
        self.assertEqual(response.status_code, 200)

        # Check that the Difficulty column header and computed value are present
        self.assertContains(response, 'Difficulty')
        self.assertContains(response, self.recipe.difficulty())
