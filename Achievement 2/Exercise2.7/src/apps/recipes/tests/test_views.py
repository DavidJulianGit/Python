from django.test import TestCase
from django.urls import reverse
from ..models import Recipe
from ..forms import RecipeForm
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.models import User



class HomeViewTests(TestCase):

    def test_home_view_no_recipes(self):
        response = self.client.get(reverse('recipe:home'))
        self.assertContains(response, 'There are no recipes in the database yet. Please add some recipes to get started.')
      
class RecipeListViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.recipe1 = Recipe.objects.create(name='Test Recipe 1', ingredients='...', cooking_time=10, directions='...')
        cls.recipe2 = Recipe.objects.create(name='Test Recipe 2', ingredients='...', cooking_time=20, directions='...')
        cls.recipe3 = Recipe.objects.create(name='Test Recipe 3', ingredients='...', cooking_time=30, directions='...')


    def test_recipe_list_view(self):
        url = reverse('recipe:recipe_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe 3')


class RecipeDetailViewTests(TestCase):

    def setUp(self):
        self.recipe = Recipe.objects.create(
            name='Test Recipe',
            ingredients='Tea Leaves, Water, Sugar',
            cooking_time=12,
            difficulty='Intermediate',
            directions='Add tea leaves to water and stir.'
        )
        self.url = reverse('recipe:recipe_detail', args=[self.recipe.pk])

    def test_recipe_detail_view(self):
        response = self.client.get(self.url)
        self.assertContains(response, 'Tea Leaves')
        self.assertContains(response, 'Water')
        self.assertContains(response, 'Sugar')
        self.assertContains(response, '12 minutes')
        self.assertContains(response, 'Intermediate')

class AddRecipeViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')
        self.url = reverse('recipe:add_recipe')
        self.valid_data = {
            'name': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'cooking_time': 30,
            'difficulty': 'Medium'
        }

    def test_add_recipe_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')

    def test_add_recipe_view_post_valid(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('recipe:add_recipe'), {
            'name': 'Test Recipe',
            'ingredients': 'Ingredient 1, Ingredient 2',
            'directions': 'Instructions',
            'cooking_time': 30,
        })
        self.assertRedirects(response, reverse('recipe:recipe_list'))

    def test_add_recipe_view_post_invalid(self):
        invalid_data = self.valid_data.copy()
        invalid_data['name'] = ''
        response = self.client.post(self.url, invalid_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'recipes/add_recipe.html')

class SearchViewTests(TestCase):

    def setUp(self):
        self.url = reverse('recipe:search')
        for i in range(5):
            Recipe.objects.create(name=f'Test Recipe {i}', ingredients='Ingredient 1', cooking_time=30, difficulty='Easy')

    def test_search_view(self):
        response = self.client.get(self.url, {'search_term': 'Test Recipe', 'searching_by': 'name'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe 0')
        self.assertContains(response, 'Test Recipe 1')
        self.assertContains(response, 'Test Recipe 2')

    def test_pagination(self):
        response = self.client.get(self.url, {'search_term': 'Test Recipe', 'searching_by': 'name', 'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Recipe 2')
        self.assertContains(response, 'Test Recipe 3')

class ChartViewTests(TestCase):

    def setUp(self):
        self.url = reverse('recipe:charts')
        Recipe.objects.create(name='Test Recipe', ingredients='Ingredient 1', cooking_time=30, difficulty='Easy')

    def test_chart_view(self):
        response = self.client.get(reverse('recipe:charts'))
        self.assertContains(response, '<img class="img-fluid my-4 w-50" src="data:image/png;base64,')
        
  
 