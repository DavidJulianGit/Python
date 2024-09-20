from django.shortcuts import render

# Create your views here.
def recipes_home(request):
    return render(request, 'recipes_home.html')