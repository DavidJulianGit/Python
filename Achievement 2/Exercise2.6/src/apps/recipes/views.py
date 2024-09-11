from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .models import Recipe
from .forms import RecipeForm
import random

# Displays a random recipe 
def home_view(request):
    recipes = Recipe.objects.all()
    if recipes:
        random_recipe = random.choice(recipes)
        context = {'recipe': random_recipe}
    else:
        context = {'no_recipes': True}
    return render(request, 'recipes/recipes_home.html', context)

# List view to show all recipes
class RecipeListView(ListView):
    model = Recipe
    template_name = 'recipes/recipe_list.html'
    context_object_name = 'recipes'

# Detail view for a single recipe
class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

# View to add a recipe
def add_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            return redirect('recipe:recipe_list')
    else:
        form = RecipeForm()
    return render(request, 'recipes/add_recipe.html', {'form': form})

