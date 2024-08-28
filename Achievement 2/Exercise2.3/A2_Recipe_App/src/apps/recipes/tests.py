from django.test import TestCase
from .models import Recipe


class RecipeModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.recipe = Recipe.objects.create(
            name="Tea",
            ingredients="Tea Leaves, Water, Sugar",
            cooking_time=4,
            difficulty="Easy"
        )
        
    def test_recipe_creation(self):
        #Test that a Recipe instance is created successfully.
        self.assertEqual(self.recipe.name, "Tea")
        self.assertEqual(self.recipe.ingredients, "Tea Leaves, Water, Sugar")
        self.assertEqual(self.recipe.cooking_time, 4)
        self.assertEqual(self.recipe.difficulty, "Easy")

    def test_recipe_str_representation(self):
        #Test the string representation of a Recipe instance.
        self.assertEqual(str(self.recipe), f"Recipe ID: {self.recipe.id} - {self.recipe.name}")

    def test_recipe_name_max_length(self):
        #Test the max length of the name field.
        max_length = self.recipe._meta.get_field('name').max_length
        self.assertEqual(max_length, 50)

    def test_recipe_ingredients_max_length(self):
        #Test the max length of the ingredients field.
        max_length = self.recipe._meta.get_field('ingredients').max_length
        self.assertEqual(max_length, 255)

    def test_recipe_difficulty_max_length(self):
        #Test the max length of the difficulty field.
        max_length = self.recipe._meta.get_field('difficulty').max_length
        self.assertEqual(max_length, 20)

