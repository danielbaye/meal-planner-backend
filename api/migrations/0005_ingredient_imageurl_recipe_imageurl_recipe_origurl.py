# Generated by Django 5.1.1 on 2024-09-12 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_ingredient_nutrition_remove_recipeingredient_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='imageUrl',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='imageUrl',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='recipe',
            name='origUrl',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
