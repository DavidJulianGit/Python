from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Recipe
from .forms import RecipeForm, RecipeSearch
from .utils import get_chart
import random
import pandas as pd
import string



def home_view(request):
    recipes = Recipe.objects.all()
    if recipes:
        random_recipe = random.choice(recipes)
        context = {'recipe': random_recipe}
    else:
        context = {'no_recipes': True}
    return render(request, 'recipes/recipes_home.html', context)

class RecipeListView(ListView):
    template_name = 'recipes/recipe_list.html'
    paginate_by = 3

    def get(self, request):
        recipes = Recipe.objects.all().order_by('name')
        page_obj = paginate_queryset(request, recipes, self.paginate_by)
        context = {
            'recipes': page_obj.object_list,
            'page_obj': page_obj,
        }
        return render(request, self.template_name, context)

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    context_object_name = 'recipe'

@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.save()
            return redirect('recipe:recipe_list')
    else:
        form = RecipeForm()
    
    return render(request, 'recipes/add_recipe.html', {'form': form})

def search_view(request):
    results = []
    form = RecipeSearch(request.POST or None)
    df = None                                                       # df dataframe
    page_number = request.GET.get('page') or 1                      # Get page number from query params

    if request.method == 'POST' and form.is_valid():
        searching_by = request.POST.get('searching_by')
        search_term = request.POST.get('search_term')

    else:
        searching_by = request.GET.get('searching_by')
        search_term = request.GET.get('search_term')

    print(search_term, searching_by, page_number)

    # Dynamically filter based on what the user is searching by
    if searching_by == 'name':  
        results = Recipe.objects.filter(name__icontains=search_term).order_by('name')
    elif searching_by == 'ingredient':  
        results = Recipe.objects.filter(ingredients__icontains=search_term).order_by('name')
    elif searching_by == 'difficulty':  
        results = Recipe.objects.filter(difficulty__iexact=search_term).order_by('name')
    elif searching_by == 'cooking_time':  
        try:
            cooking_time = int(search_term)
            results = Recipe.objects.filter(cooking_time=cooking_time).order_by('name')
        except ValueError:
            results = []  

    
    # Paginate results
    paginator = Paginator(results, 3)  
    page_obj = paginator.get_page(page_number)
    
    print(paginator, page_obj)

    if results:
        df = pd.DataFrame(results.values())    

        # DataFrame transformations
        df['name'] = df.apply(make_clickable_name, axis=1)
        df['cooking_time'] = df['cooking_time'].astype(str) + ' min'  # Format cooking time
        
        # Drop columns you don't want to display
        df = df[['name', 'ingredients', 'cooking_time', 'difficulty']]

        # Convert to HTML table with styling options
        df = df.to_html( 
            classes='table table-striped table-hover bg-transparent text-light',
            index=False,  # Hide the index column
            justify='start',  # Center-align the table content
            border=0,
            render_links=True,  # Enable clickable links if you have URLs
            escape=False  # Avoid escaping HTML (e.g., if you want to render images or links)
        )
    
    context = {
        'form': form,
        'results': page_obj.object_list,
        'page_obj': page_obj,
        'df':df,
        'search_term': search_term,
        'searching_by': searching_by,
    }

    return render(request, 'recipes/search.html', context)

def chart_view(request):
    chart = None
    df = None
    qs = Recipe.objects.all().values()
    
    if qs:                
        pie_chart = get_chart('PC', qs)
        bar_chart = get_chart('BC', qs)
        line_chart= get_chart('LC', qs)
    
    context = {
        'pie_chart': pie_chart,
        'bar_chart': bar_chart,
        'line_chart': line_chart
    }
    return render(request, 'recipes/recipe_charts.html', context)

# # Helper functions
# create clickable links for the recipe name
def make_clickable_name(row):
    url = reverse('recipe:recipe_detail', args=[row['id']])
    return f'<a href="{url}">{string.capwords(row["name"])}</a>'

# pagination
def paginate_queryset(request, queryset, paginate_by):
    paginator = Paginator(queryset, paginate_by)
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)
    return page_obj