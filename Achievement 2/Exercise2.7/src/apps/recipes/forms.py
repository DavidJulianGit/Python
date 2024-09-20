from django import forms                        # modelForms are directly tied to Django models.
from .models import Recipe
from django.forms import widgets
from markdownx.fields import MarkdownxFormField


class RecipeForm(forms.ModelForm):
    directions = MarkdownxFormField()
    
    # meta information
    class Meta:
        model = Recipe
        fields = ['name', 'ingredients', 'cooking_time', 'directions', 'image']
      

SEARCHING_BY_CHOICES = (
    ('name', 'Name'),
    ('ingredient', "Ingredient"),    
    ('cooking_time', "Cooking Time"),  
    ('difficulty', 'Difficulty')
)
class RecipeSearch(forms.Form):
    searching_by = forms.ChoiceField(choices=SEARCHING_BY_CHOICES)
    search_term = forms.CharField(max_length=120)