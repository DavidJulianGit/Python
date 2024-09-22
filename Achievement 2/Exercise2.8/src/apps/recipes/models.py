from django.db import models


# Create your models here.
class Recipe(models.Model):
    name = models.CharField(max_length=55)
    ingredients = models.CharField(max_length=255)
    cooking_time = models.IntegerField()
    difficulty = models.CharField(max_length=20, editable=False)
    directions = models.TextField(max_length=2000, default="")
    image = models.ImageField(upload_to="recipe_images", default="no_picture.jpg")

    def save(self, *args, **kwargs):
        self.calculate_difficulty()
        super().save(*args, **kwargs)

    def return_ingredients_as_list(self):
        return [ingredient.strip() for ingredient in self.ingredients.split(",")]

    def calculate_difficulty(self):
        cooking_time = int(self.cooking_time)
        num_ingredients = len(self.return_ingredients_as_list())

        if cooking_time < 10 and num_ingredients < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and num_ingredients >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and num_ingredients < 4:
            difficulty = "Intermediate"
        else:
            difficulty = "Hard"

        self.difficulty = difficulty

    def __str__(self):
        return f"Recipe ID: {self.id} - {self.name}"
