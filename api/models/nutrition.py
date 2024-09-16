from django.db import models



class Nutrition(models.Model):
    #nutrition is in grams per 100 grams, wether recepie or ingridient
    calories = models.FloatField()
    proteinGram = models.FloatField()
    carbsGram = models.FloatField()
    fatGram = models.FloatField()
    saturatedFatGram = models.FloatField()
    saltGram = models.FloatField()
    
    def __str__(self):
        return f"Nutrition: {self.calories} kcal, {self.fatGram}g fat, {self.proteinGram}g protein, {self.carbsGram}g carbs, {self.saltGram}g salt"