from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import RecipeListView, RecipeDetailView

class RecipeURLsTest(SimpleTestCase):
    def test_recipe_list_url(self):
        url = reverse('recipe:recipe_list')
        self.assertEqual(resolve(url).func.view_class, RecipeListView)

    def test_recipe_detail_url(self):
        url = reverse('recipe:recipe_detail', args=[1])
        self.assertEqual(resolve(url).func.view_class, RecipeDetailView)
