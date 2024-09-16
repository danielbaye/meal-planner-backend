from django.db import models


class SkillLevel(models.Model):
    level = models.IntegerField()
    name = models.TextField(max_length=10)

    def __str__(self):
        return f"name: {self.name}: level:{self.level}"
