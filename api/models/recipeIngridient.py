from django.db import models

from api.models.recipe import Recipe


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='ingredients', on_delete=models.CASCADE)  # One-to-Many relationship with Recipe
    name = models.CharField(max_length=255)
    quantity = models.CharField(max_length=100)  # Example: "2 cups", "1 tsp"

    def __str__(self):
        return f"{self.quantity} of {self.name}"