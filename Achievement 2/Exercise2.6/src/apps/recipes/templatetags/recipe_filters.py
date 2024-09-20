from django import template

register = template.Library()

@register.filter
def split_ingredients(value):
 
    # Split the ingredients string by commas and return as a list.
    return value.split(', ')

@register.filter
def style_difficulty(value):
    
    difficulty_classes = {
        'Easy': 'btn-success',
        'Medium': 'btn-warning',
        'Intermediate': 'btn-danger',
        'Hard': 'btn-primary'
    }

    return difficulty_classes.get(value, '')

