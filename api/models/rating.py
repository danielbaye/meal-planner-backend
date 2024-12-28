from django.db import models
from django.contrib.auth.models import User

from api.models.recipe import Recipe
from django.utils import timezone


class Rating(models.Model):
    user = models.ForeignKey(User,
                             related_name='ratings',
                             on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe,
                               related_name='ratings',
                               on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(choices=[(i, str(i))
                                                 for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'recipe')

    def __str__(self):
        return f"{self.user.username} rated {self.recipe.title} - {self.stars} stars"
