from django.db import models
from django.contrib.auth.models import User

from .nutrition import Nutrition
from .tag import Tag
from .skill_level import SkillLevel
# Create your models here.


class Recipe(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='recipes', blank=True)
    skill_level = models.ForeignKey(SkillLevel,
                                    related_name='recipes',
                                    on_delete=models.CASCADE,
                                    null=True)
    dishNumber = models.IntegerField(default=1)
    preparationMinutes = models.IntegerField(default=0)
    nutrition = models.OneToOneField(Nutrition,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True)  # One-to-one with Nutrition
    imageUrl = models.CharField(null=True)
    origUrl = models.CharField(null=True)
    source = models.CharField(max_length=50, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title', 'source'],
                                    name='unique_recipe_title_source')
        ]

    def __str__(self):
        return f"{self.title}, skill level:{self.skillLevel}, dishNumber: {self.dishNumber}, preperatation minutes: {self.preparationMinutes}, nutrition: {self.nutrition}, tags: {self.tags}"
