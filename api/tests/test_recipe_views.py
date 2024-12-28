from django.test import Client, TestCase
from django.urls import resolve, reverse

from api.models.method import Method
from api.models.nutrition import Nutrition
from api.models.recipe import Recipe
from api.models.skill_level import SkillLevel
from api.models.tag import Tag
from api.views import GetRecipes


class TestViews(TestCase):

    def setUp(self) -> None:
        self.client = Client()
        self.skill_level = SkillLevel.objects.create(level=2,
                                                     name='Intermediate')

        # Create a Nutrition instance
        self.nutrition = Nutrition.objects.create(calories=250.0,
                                                  proteinGram=10.0,
                                                  carbsGram=30.0,
                                                  fatGram=8.0,
                                                  saturatedFatGram=3.0,
                                                  saltGram=0.5)

        # Create Tag instances
        self.tag1 = Tag.objects.create(name='Vegetarian')
        self.tag2 = Tag.objects.create(name='Quick')

        # Create 10 Recipe instances with demo data
        self.recipes = []
        for i in range(10):
            nutrition = Nutrition.objects.create(calories=250.0 * (1 + i),
                                                 proteinGram=10.0,
                                                 carbsGram=30.0,
                                                 fatGram=8.0,
                                                 saturatedFatGram=3.0,
                                                 saltGram=0.5)
            recipe = Recipe.objects.create(
                title=f"Recipe {i + 1}",
                description=f"This is a description for recipe {i + 1}.",
                skill_level=self.skill_level,
                dishNumber=i + 1,
                preparationMinutes=i * 5,
                nutrition=nutrition,
                imageUrl=f"http://example.com/image_{i + 1}.jpg",
                origUrl=f"http://example.com/recipe-url-{i + 1}",
                source="Recipe Source",
                approximate_cost=10.00 + (i * 0.5))
            # Add tags to the recipe
            recipe.tags.add(self.tag1, self.tag2)
            self.recipes.append(recipe)

            # Create Method instances related to the recipe
            Method.objects.create(recipe=recipe,
                                  text=f"Step 1 for Recipe {i + 1}.",
                                  step=1)
            Method.objects.create(recipe=recipe,
                                  text=f"Step 2 for Recipe {i + 1}.",
                                  step=2)
        return super().setUp()

    def test_recipes_url_resolves(self):
        # Test URL resolution for each recipe
        url = reverse('recipes-list')
        resolved_view = resolve(url)
        self.assertEqual(resolved_view.func.view_class, GetRecipes)

    def test_recipes_get(self):
        # Test if we can access the 'GetRecipes' view through the Client for each recipe
        for i, recipe in enumerate(self.recipes):
            url = reverse('recipes-list-id', kwargs={'id': recipe.id})
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()['title'], f"Recipe {i+1}")

    def test_register_get(self):
        url = reverse('register')
        data = {"username": "name", "password": "pass", "email": "asd@asd.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        url = reverse('register')
        data = {"username": "name", "password": "pass", "email": "asd@asd.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)

        url = reverse('login')
        data = {"password": "pass", "email": "asd@asd.com"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 400)
