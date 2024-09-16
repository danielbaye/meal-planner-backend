from django.db import models

from .nutrition import Nutrition


class Ingredient(models.Model):
    nutrition = models.OneToOneField(Nutrition,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True)  # One-to-one with Nutrition

    name = models.CharField(max_length=255)
    externalId = models.CharField(max_length=255)
    imageUrl = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"{self.name}"
