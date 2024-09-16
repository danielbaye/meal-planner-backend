from django.db import models

from .ingridient import Ingredient
from .recipe import Recipe


class RecipeIngredient(models.Model):

    GRAM = 'g'
    MILILITER = "ml"
    SINGLE = ""
    MEASUREMENT_CHOICES = [
        (GRAM, 'g'),
        (MILILITER, 'ml'),
        (SINGLE, ''),
    ]
    recipe = models.ForeignKey(
        Recipe, related_name='recipe_ingredients',
        on_delete=models.CASCADE)  # One-to-many with Recipe
    ingredient = models.ForeignKey(Ingredient,
                                   related_name='recipe_ingredients',
                                   on_delete=models.CASCADE,
                                   null=True)  # Many-to-one with Ingredient
    quantity = models.FloatField()  #always in grams
    measurement = models.CharField(max_length=20, default='')
    text = models.TextField(max_length=100, default='')

    def __str__(self):
        return f"{self.quantity} {self.measurement} of {self.ingredient.name}"
