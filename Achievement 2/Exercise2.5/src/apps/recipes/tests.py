from django.test import Client, TestCase
from django.urls import reverse
from .models import Recipe

class RecipeModelTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="ingredient1, ingredient2, ingredient3",
            cooking_time=20,
            directions="Test directions"
        )

    def test_create_recipe(self):
        self.assertEqual(Recipe.objects.count(), 1)
        self.assertEqual(self.recipe.name, "Test Recipe")

    def test_return_ingredients_as_list(self):
        ingredients = self.recipe.return_ingredients_as_list()
        self.assertEqual(ingredients, ["ingredient1", "ingredient2", "ingredient3"])

    def test_calculate_difficulty(self):
        self.recipe.calculate_difficulty()
        self.assertEqual(self.recipe.difficulty, "Intermediate")

class RecipeListViewTests(TestCase):
    def test_no_recipes(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, "There are no recipes in the database yet")
        self.assertNotContains(response, "Recipe of the Day")

    def test_recipes_list(self):
        recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="ingredient1, ingredient2, ingredient3",
            cooking_time=20,
            directions="Test directions"
        )
        response = self.client.get(reverse('recipe:recipe_list'))
        self.assertContains(response, recipe.name)

class RecipeDetailViewTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="ingredient1, ingredient2, ingredient3",
            cooking_time=20,
            directions="Test directions"
        )

    def test_valid_recipe(self):
        response = self.client.get(reverse('recipe:recipe_detail', args=[self.recipe.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.recipe.name)

    def test_invalid_recipe(self):
        response = self.client.get(reverse('recipe:recipe_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

class AddRecipeViewTests(TestCase):
    def test_valid_form(self):
        data = {
            'name': 'Test Recipe',
            'ingredients': 'ingredient1, ingredient2, ingredient3',
            'cooking_time': 20,
            'directions': 'Test directions'
        }
        response = self.client.post(reverse('recipe:add_recipe'), data)
        self.assertRedirects(response, reverse('recipe:recipe_list'))
        self.assertEqual(Recipe.objects.count(), 1)

    def test_invalid_form(self):
        data = {
            'name': '',
            'ingredients': '',
            'cooking_time': -10,
            'directions': ''
        }
        response = self.client.post(reverse('recipe:add_recipe'), data)
        self.assertContains(response, 'name')
        self.assertContains(response, 'ingredients')
        self.assertContains(response, 'cooking_time')
        self.assertContains(response, 'directions')
        self.assertEqual(Recipe.objects.count(), 0)