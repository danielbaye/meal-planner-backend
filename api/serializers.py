from django.contrib.auth.models import User
from api.models.ingridient import Ingredient
from api.models.method import Method
from api.models.nutrition import Nutrition
from api.models.recipe import Recipe
from api.models.skill_level import SkillLevel
from api.models.tag import Tag
from api.models.recipeIngridient import RecipeIngredient
from rest_framework import serializers

from api.models.note import Note


class UserSerianizer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwarsd = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}


class MethodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Method
        fields = ['step', 'text']


class NutritionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nutrition
        fields = [
            'calories', 'proteinGram', 'carbsGram', 'fatGram',
            'saturatedFatGram', 'saltGram'
        ]


class IngredientSerializer(serializers.ModelSerializer):
    nutrition = NutritionSerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = ['name', 'externalId', 'imageUrl', 'nutrition']


class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer(
        read_only=True)  # Nested Ingredient serializer

    class Meta:
        model = RecipeIngredient
        fields = ["quantity", "measurement", "ingredient", "text"]


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']


class skillLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = SkillLevel
        fields = ['level', 'name']


class RecipeSerializer(serializers.ModelSerializer):
    methods = MethodSerializer(many=True, read_only=True)
    recipe_ingredients = RecipeIngredientSerializer(many=True, read_only=True)
    nutrition = NutritionSerializer(read_only=True)
    skillLevel = skillLevelSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'dishNumber', 'preparationMinutes',
            'methods', 'recipe_ingredients', 'nutrition', 'skill_level',
            'skillLevel', 'tags', 'imageUrl', 'origUrl'
        ]


class SimplifiedRecipeSerializer(serializers.ModelSerializer):
    skillLevel = skillLevelSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = [
            'title', 'description', 'dishNumber', 'preparationMinutes',
            'skill_level', 'skillLevel', 'imageUrl', 'id'
        ]
