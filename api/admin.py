from django.contrib import admin
from .models.recipe import Recipe  # Import your model


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'dishNumber', 'preparationMinutes',
                    'nutrition')  # Columns to display
    search_fields = ('title', )  # Add search functionality
    list_filter = ('title', )  # Filters on the right sidebar


# Register your models here.
