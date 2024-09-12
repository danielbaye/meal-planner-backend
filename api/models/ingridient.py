from django.db import models



class Ingredient(models.Model):
    
    name = models.CharField(max_length=255)
    externalId = models.CharField(max_length=255,unique=True)
    

    def __str__(self):
        return f"{self.name}"