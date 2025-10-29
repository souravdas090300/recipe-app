from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from recipe.models import Recipe


User = get_user_model()


class RecipeListDetailViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='viewer', email='viewer@example.com', password='pass1234'
        )
        # Create two recipes
        self.r1 = Recipe.objects.create(
            name='Pasta Primavera',
            cooking_time=8,
            ingredients='pasta, tomato, basil, garlic',
            description='Light pasta with veggies',
            user=self.user,
        )
        self.r2 = Recipe.objects.create(
            name='Roast Chicken',
            cooking_time=60,
            ingredients='chicken, salt, pepper, lemon, thyme',
            user=self.user,
        )

    def test_get_absolute_url(self):
        self.assertEqual(
            self.r1.get_absolute_url(),
            reverse('recipe:recipe-detail', kwargs={'pk': self.r1.pk}),
        )

    def test_recipes_list_view(self):
        url = reverse('recipe:recipes-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'recipe/recipes_list.html')
        # Contains links to detail pages
        self.assertContains(resp, self.r1.name)
        self.assertContains(resp, self.r2.name)
        self.assertContains(resp, self.r1.get_absolute_url())
        self.assertContains(resp, self.r2.get_absolute_url())

    def test_recipe_detail_view(self):
        url = reverse('recipe:recipe-detail', kwargs={'pk': self.r2.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'recipe/recipe_detail.html')
        # Fields rendered
        self.assertContains(resp, self.r2.name)
        self.assertContains(resp, str(self.r2.cooking_time))
        # Difficulty should render via method
        self.assertContains(resp, self.r2.difficulty())
