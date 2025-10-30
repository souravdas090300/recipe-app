from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipe.models import Recipe


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
