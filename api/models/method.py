from django.db import models

from .recipe import Recipe


class Method(models.Model):
    recipe = models.ForeignKey(
        Recipe, related_name='methods',
        on_delete=models.CASCADE)  # One-to-Many relationship with Recipe
    text = models.CharField()
    step = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['recipe', 'step'],
                                    name='unique_recipe_step')
        ]

    def __str__(self):
        return f"{self.quantity} of {self.name}"
