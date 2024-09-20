from django import forms
from .models import Recipe
from django.forms import widgets
from markdownx.fields import MarkdownxFormField

class RecipeForm(forms.ModelForm):
    directions = MarkdownxFormField()

    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'cooking_time', 'directions', 'image']
