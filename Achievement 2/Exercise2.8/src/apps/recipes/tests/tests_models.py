from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import Client, TestCase
from django.urls import reverse
from ..models import Recipe


class RecipeModelTests(TestCase):
    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Test Recipe",
            ingredients="ingredient1, ingredient2, ingredient3",
            cooking_time=20,
            directions="Test directions",
            image=SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
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

    def test_str_method(self):
        self.assertEqual(str(self.recipe), f"Recipe ID: {self.recipe.id} - Test Recipe")

    def test_fields(self):
        self.assertEqual(self.recipe.name, 'Test Recipe')
        self.assertEqual(self.recipe.ingredients, 'ingredient1, ingredient2, ingredient3')
        self.assertEqual(self.recipe.cooking_time, 20)
        self.assertEqual(self.recipe.directions, 'Test directions')
        self.assertTrue(self.recipe.image)  

