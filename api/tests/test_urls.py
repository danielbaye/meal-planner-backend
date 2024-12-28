from django.test import SimpleTestCase
from django.urls import resolve, reverse

from api.auth.views import UserRegistrationView
from api.views import GetRecipeSuggestions, GetRecipes, IngridientScrapeView, RecipeScrapeView


class TestUrls(SimpleTestCase):

    def test_url_recipes_list_resolved(self):
        url = reverse('recipes-list')
        self.assertEqual(resolve(url).func.view_class, GetRecipes)

    def test_url_recipes_list_id_resolved(self):
        recipe_id = 1
        url = reverse('recipes-list-id', kwargs={'id': recipe_id})
        self.assertEqual(resolve(url).func.view_class, GetRecipes)

    def test_url_suggestions_resolved(self):
        url = reverse('recipes-search-suggestions')
        self.assertEqual(resolve(url).func.view_class, GetRecipeSuggestions)

    def test_register_resolved(self):
        url = reverse('register')
        print(url)
        self.assertEqual(resolve(url).func.view_class, UserRegistrationView)

    # def test_url_scrape_recipe_resolved(self):
    #     url = reverse('scrape-recipe')
    #     self.assertEqual(resolve(url).func.view_class, RecipeScrapeView)

    # def test_url_scrape_ingridients_resolved(self):
    #     url = reverse('scrape-ingridient')
    #     self.assertEqual(resolve(url).func.view_class, IngridientScrapeView)
