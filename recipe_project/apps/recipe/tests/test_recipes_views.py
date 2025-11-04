from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.recipe.models import Recipe


User = get_user_model()


class RecipeListDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='viewer', email='viewer@example.com', password='pass1234'
        )
        # Create a couple of recipes
        self.r1 = Recipe.objects.create(
            name='Pasta', cooking_time=12, ingredients='pasta, salt, oil', user=self.user
        )
        self.r2 = Recipe.objects.create(
            name='Salad', cooking_time=5, ingredients='lettuce, tomato, olive oil, salt', user=self.user
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.r1.get_absolute_url(), f"/recipes/{self.r1.pk}/")

    def test_list_view_status_and_template(self):
        # Log in before accessing protected view
        self.client.login(username='viewer', password='pass1234')
        url = reverse('recipe:recipes-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'recipe/recipes_list.html')
        # Names should appear
        self.assertContains(resp, 'Pasta')
        self.assertContains(resp, 'Salad')
        # Links should point to detail pages
        self.assertContains(resp, self.r1.get_absolute_url())
        self.assertContains(resp, self.r2.get_absolute_url())

    def test_detail_view_status_and_template(self):
        # Log in before accessing protected view
        self.client.login(username='viewer', password='pass1234')
        url = reverse('recipe:recipe-detail', kwargs={'pk': self.r1.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'recipe/recipe_detail.html')
        # Page should show fields and computed difficulty label
        self.assertContains(resp, 'Pasta')
        self.assertContains(resp, 'Cooking Time')
        self.assertContains(resp, 'Difficulty')


class RecipeSearchTests(TestCase):
    """Test cases for recipe search functionality."""

    def setUp(self):
        """Set up test user and recipes."""
        self.user = User.objects.create_user(
            username='searcher', email='searcher@example.com', password='test1234'
        )
        # Create recipes with different characteristics
        self.recipe1 = Recipe.objects.create(
            name='Spaghetti Carbonara',
            cooking_time=25,
            ingredients='spaghetti, eggs, bacon, parmesan, pepper',
            user=self.user,
            category='dinner'
        )
        self.recipe2 = Recipe.objects.create(
            name='Caesar Salad',
            cooking_time=8,
            ingredients='lettuce, croutons',
            user=self.user,
            category='lunch'
        )
        self.recipe3 = Recipe.objects.create(
            name='Chocolate Cake',
            cooking_time=45,
            ingredients='flour, cocoa',
            user=self.user,
            category='dessert'
        )

    def test_search_form_appears_on_list_view(self):
        """Test that search form appears on the recipes list page."""
        self.client.login(username='searcher', password='test1234')
        url = reverse('recipe:recipes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'recipe_name')
        self.assertContains(response, 'chart_type')
        self.assertContains(response, 'difficulty')

    def test_search_by_exact_name(self):
        """Test searching for a recipe by exact name."""
        self.client.login(username='searcher', password='test1234')
        url = reverse('recipe:recipes-list')
        response = self.client.post(url, {
            'recipe_name': 'Caesar Salad',
            'chart_type': '#1',
            'difficulty': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Caesar Salad')

    def test_search_by_partial_name(self):
        """Test searching with partial/wildcard search."""
        self.client.login(username='searcher', password='test1234')
        url = reverse('recipe:recipes-list')
        response = self.client.post(url, {
            'recipe_name': 'Salad',
            'chart_type': '#2',
            'difficulty': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Caesar Salad')

    def test_search_case_insensitive(self):
        """Test that search is case-insensitive."""
        self.client.login(username='searcher', password='test1234')
        url = reverse('recipe:recipes-list')
        response = self.client.post(url, {
            'recipe_name': 'SPAGHETTI',
            'chart_type': '#3',
            'difficulty': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Spaghetti Carbonara')

    def test_search_by_difficulty_easy(self):
        """Test searching by difficulty level - Easy."""
        self.client.login(username='searcher', password='test1234')
        url = reverse('recipe:recipes-list')
        response = self.client.post(url, {
            'recipe_name': '',
            'chart_type': '#1',
            'difficulty': 'Easy'
        })
        self.assertEqual(response.status_code, 200)
        # Caesar Salad should be Easy (8 min, 2 ingredients)

    def test_search_no_results(self):
        """Test search with no matching results."""
        self.client.login(username='searcher', password='test1234')
        url = reverse('recipe:recipes-list')
        response = self.client.post(url, {
            'recipe_name': 'NonExistentRecipe',
            'chart_type': '#1',
            'difficulty': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No recipes found')

    def test_search_all_recipes_empty_name(self):
        """Test that empty recipe name returns all recipes."""
        self.client.login(username='searcher', password='test1234')
        url = reverse('recipe:recipes-list')
        response = self.client.post(url, {
            'recipe_name': '',
            'chart_type': '#2',
            'difficulty': ''
        })
        self.assertEqual(response.status_code, 200)
        # Should show all three recipes
        self.assertContains(response, 'Spaghetti Carbonara')
        self.assertContains(response, 'Caesar Salad')
        self.assertContains(response, 'Chocolate Cake')

    def test_chart_generation_bar_chart(self):
        """Test that bar chart is generated."""
        self.client.login(username='searcher', password='test1234')
        url = reverse('recipe:recipes-list')
        response = self.client.post(url, {
            'recipe_name': '',
            'chart_type': '#1',
            'difficulty': ''
        })
        self.assertEqual(response.status_code, 200)
        # Check for chart image tag
        self.assertContains(response, 'data:image/png;base64')

    def test_chart_generation_pie_chart(self):
        """Test that pie chart is generated."""
        self.client.login(username='searcher', password='test1234')
        url = reverse('recipe:recipes-list')
        response = self.client.post(url, {
            'recipe_name': 'Salad',
            'chart_type': '#2',
            'difficulty': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data:image/png;base64')

    def test_chart_generation_line_chart(self):
        """Test that line chart is generated."""
        self.client.login(username='searcher', password='test1234')
        url = reverse('recipe:recipes-list')
        response = self.client.post(url, {
            'recipe_name': '',
            'chart_type': '#3',
            'difficulty': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'data:image/png;base64')

    def test_unauthenticated_user_redirected(self):
        """Test that unauthenticated users are redirected to login."""
        url = reverse('recipe:recipes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)
