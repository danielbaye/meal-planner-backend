from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Recipe(models.Model):
    
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
    EXPERT = 'expert'

    SKILL_LEVEL_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCED, 'Advanced'),
        (EXPERT, 'Expert'),
    ]
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    tags = models.ManyToManyField('Tag', related_name='recipes', blank=True) 
    skillLevel = models.CharField(
        max_length=12, 
        choices=SKILL_LEVEL_CHOICES, 
        default=BEGINNER
    )
    dishNumber = models.IntegerField(default=1) 
    preparationMinutes = models.IntegerField(default=0) 

    def __str__(self):
        return self.title