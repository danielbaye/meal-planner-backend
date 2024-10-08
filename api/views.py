from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from scraper.Scraper.ingridient_scraper import parseIngridient

from .services.recipe import add_approximate_cost_to_recipe, getRecipes, scrape_all_recipes, scrape_and_save_recipe
from rest_framework import generics
from django.http import JsonResponse
from api.models.note import Note
from api.models.recipeIngridient import RecipeIngredient
from api.models.recipe import Recipe
from api.models.ingridient import Ingredient
from django.contrib.postgres.search import TrigramSimilarity

from .serializers import NoteSerializer, RecipeSerializer, RecipeSuggestionSerializer, SimplifiedRecipeSerializer, UserSerianizer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views import View


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerianizer
    permission_classes = [AllowAny]


class NoteListCreate(generics.ListCreateAPIView):
    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(author=self.request.user)
        else:
            print(serializer.errors)


class NoteDelete(generics.DestroyAPIView):

    serializer_class = NoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(author=user)


class GetRecipeSuggestions(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        searchString = request.GET.get('searchString')
        num_to_load = int(request.GET.get('num_to_load', 5))
        recipeSuggestions = Recipe.get_similar_recipes(searchString,
                                                       num_to_load)
        serializer = RecipeSuggestionSerializer(recipeSuggestions, many=True)
        return JsonResponse(serializer.data, safe=False)


class GetRecipes(generics.ListAPIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        recipe_id = kwargs.get('id')
        lastId = int(request.GET.get('lastId', 0))
        num_to_load = int(request.GET.get('num_to_load', 0))

        if recipe_id:
            # Get a specific recipe by ID
            recipe = get_object_or_404(Recipe, id=recipe_id)
            serializer = RecipeSerializer(recipe)
            return JsonResponse(serializer.data)
        elif lastId != None and num_to_load:
            recipes = Recipe.objects.filter(
                id__gt=lastId).order_by('id')[:num_to_load]
            serializer = SimplifiedRecipeSerializer(recipes, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            # Get all recipes
            recipes = Recipe.objects.all()
            serializer = RecipeSerializer(recipes, many=True)
            return JsonResponse(serializer.data, safe=False)

    queryset = getRecipes()  # Recipe.objects.all()  # Fetch all Recipe objects
    serializer_class = RecipeSerializer  # Specify the serializer class


class RecipeScrapeView(View):

    def get(self, request):
        url = request.GET.get('url')
        if url:
            try:
                scrape_and_save_recipe(url)
                return JsonResponse({
                    'status': 'success',
                    'message': 'Recipe saved successfully'
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                },
                                    status=500)
        else:
            try:
                scrape_all_recipes()
                return JsonResponse({
                    'status': 'success',
                    'message': 'all recipes scraped'
                })
            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e)
                },
                                    status=500)

    serializer_class = RecipeSerializer  # Specify the serializer class
    permission_classes = [AllowAny]


class IngridientScrapeView(View):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        name = kwargs.get('name')
        if name == 'cost':
            add_approximate_cost_to_recipe()
        elif name != 'all':
            ingridient = Ingredient.objects.filter(name=name).first()
            if not ingridient:
                return JsonResponse({'error': "no such ingridient"},
                                    safe=False)
            return JsonResponse(parseIngridient(ingridient), safe=False)
        else:
            ingridients = Ingredient.objects.filter(heb_name=None)
            updatedIngridients = []
            for ingridient in ingridients:
                was_parsed = parseIngridient(ingridient)
                if was_parsed:
                    updatedIngridients.append(ingridient.name)
            return JsonResponse(updatedIngridients, safe=False)
