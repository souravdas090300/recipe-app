from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.recipe.models import Recipe


User = get_user_model()


class RecipeListDetailTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='lister', email='lister@example.com', password='pass1234'
        )
        # Create some recipes
        self.r1 = Recipe.objects.create(
            name='Pasta', cooking_time=8, ingredients='pasta, salt, water', user=self.user
        )
        self.r2 = Recipe.objects.create(
            name='Salad', cooking_time=5, ingredients='lettuce, tomato, oil, salt', user=self.user
        )

    def test_get_absolute_url(self):
        self.assertEqual(self.r1.get_absolute_url(), f"/recipes/{self.r1.pk}/")

    def test_recipes_list_view(self):
        # Log in before accessing protected view
        self.client.login(username='lister', password='pass1234')
        url = reverse('recipe:recipes-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/recipes_list.html')
        # Should list recipe names and link to details
        self.assertContains(response, self.r1.name)
        self.assertContains(response, self.r2.name)
        self.assertContains(response, self.r1.get_absolute_url())
        self.assertContains(response, self.r2.get_absolute_url())

    def test_recipe_detail_view(self):
        # Log in before accessing protected view
        self.client.login(username='lister', password='pass1234')
        url = reverse('recipe:recipe-detail', kwargs={'pk': self.r2.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipe/recipe_detail.html')
        # Contains detail fields and computed difficulty
        self.assertContains(response, self.r2.name)
        self.assertContains(response, str(self.r2.cooking_time))
        self.assertContains(response, self.r2.difficulty())
