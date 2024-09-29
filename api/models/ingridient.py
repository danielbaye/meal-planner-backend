from django.db import models

from .nutrition import Nutrition


class Ingredient(models.Model):
    nutrition = models.OneToOneField(Nutrition,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True)  # One-to-one with Nutrition

    name = models.CharField(max_length=255)
    externalId = models.CharField(max_length=255, null=True)
    imageUrl = models.CharField(max_length=255, null=True)
    heb_name = models.CharField(max_length=255, null=True)
    cost_per_100_gr_ml = models.DecimalField(default=0,
                                             max_digits=4,
                                             decimal_places=2)

    def __str__(self):
        return f"{self.name}"
