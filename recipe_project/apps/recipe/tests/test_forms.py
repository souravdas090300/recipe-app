from django.test import TestCase
from django.contrib.auth.models import User
from apps.recipe.models import Recipe
from apps.recipe.forms import RecipeSearchForm


class RecipeFormTest(TestCase):
    """Test cases for RecipeSearchForm."""

    def test_form_renders_recipe_name_input(self):
        """Test that recipe_name field is rendered correctly."""
        form = RecipeSearchForm()
        self.assertIn('recipe_name', form.fields)
        self.assertEqual(form.fields['recipe_name'].max_length, 120)
        self.assertFalse(form.fields['recipe_name'].required)

    def test_form_renders_chart_type_select(self):
        """Test that chart_type field is rendered correctly."""
        form = RecipeSearchForm()
        self.assertIn('chart_type', form.fields)
        # Should have 3 choices: bar, pie, line
        self.assertEqual(len(form.fields['chart_type'].choices), 3)

    def test_form_renders_difficulty_select(self):
        """Test that difficulty field is rendered correctly."""
        form = RecipeSearchForm()
        self.assertIn('difficulty', form.fields)
        # Should have 5 choices: All, Easy, Medium, Intermediate, Hard
        self.assertEqual(len(form.fields['difficulty'].choices), 5)
        self.assertFalse(form.fields['difficulty'].required)

    def test_form_valid_with_all_fields(self):
        """Test form is valid when all fields are provided."""
        form_data = {
            'recipe_name': 'Pasta',
            'chart_type': '#1',
            'difficulty': 'Easy'
        }
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_valid_with_empty_recipe_name(self):
        """Test form is valid even when recipe_name is empty (show all)."""
        form_data = {
            'recipe_name': '',
            'chart_type': '#2',
            'difficulty': ''
        }
        form = RecipeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_without_chart_type(self):
        """Test form is invalid when chart_type is missing."""
        form_data = {
            'recipe_name': 'Pasta',
            'difficulty': 'Easy'
        }
        form = RecipeSearchForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_form_chart_type_choices(self):
        """Test that chart_type has correct choices."""
        form = RecipeSearchForm()
        choices = form.fields['chart_type'].choices
        choice_values = [choice[0] for choice in choices]
        self.assertIn('#1', choice_values)  # Bar chart
        self.assertIn('#2', choice_values)  # Pie chart
        self.assertIn('#3', choice_values)  # Line chart

    def test_form_difficulty_choices(self):
        """Test that difficulty has correct choices."""
        form = RecipeSearchForm()
        choices = form.fields['difficulty'].choices
        choice_values = [choice[0] for choice in choices]
        self.assertIn('', choice_values)  # All
        self.assertIn('Easy', choice_values)
        self.assertIn('Medium', choice_values)
        self.assertIn('Intermediate', choice_values)
        self.assertIn('Hard', choice_values)
