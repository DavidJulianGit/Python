from django.urls import path
from .views import RecipeListView, RecipeDetailView, add_recipe, home_view, search_view, chart_view

app_name = 'recipe'

urlpatterns = [
    path('', home_view, name='home'), 
    path('list/', RecipeListView.as_view(), name='recipe_list'), 
    path('<int:pk>/', RecipeDetailView.as_view(), name='recipe_detail'),  
    path('add/', add_recipe, name='add_recipe'),
    path('search/', search_view, name='search'),
    path('charts/', chart_view, name='charts')
]
