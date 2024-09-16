from api.models.recipe import Recipe
from api.models.nutrition import Nutrition as NutritionRepository
from api.models.recipeIngridient import RecipeIngredient
from api.models.skill_level import SkillLevel
from api.models.tag import Tag
from api.models.method import Method
from api.models.ingridient import Ingredient
from scraper.Scraper.read_Jamie import JamieScraper
from scraper.Scraper.types.ingridient import parsedIngridient
from scraper.Scraper.types.scraper_types import ParsedRecipe
from scraper.Utils.types.nutrition_empty import Nutrition


def getRecipes():
    recipes = Recipe.objects.all()
    return recipes


def getRecipeById(recipe_id: int):
    recipes = Recipe.objects.get(id=recipe_id)
    return recipes


def scrape_and_save_recipe(url: str):
    jamieScraper = JamieScraper()
    recipe = jamieScraper.get_formatted_recipe(url)
    saved_recipe = save_recipe(recipe)
    return saved_recipe


def scrape_all_recipes():
    jamieScraper = JamieScraper()
    urlList = jamieScraper.getUrlList()
    for url in urlList:
        recipe = jamieScraper.get_formatted_recipe(url)
        if recipe:
            save_recipe(recipe)


def save_nutrition(nutrition: Nutrition):
    return NutritionRepository.objects.create(
        calories=nutrition.caloriesGram,
        proteinGram=nutrition.proteinGram,
        carbsGram=nutrition.carbsGram,
        fatGram=nutrition.fatGram,
        saturatedFatGram=nutrition.saturatedFatGram,
        saltGram=nutrition.saltGram,
    )


def get_skillLevel(skillLevel: int):
    try:
        return SkillLevel.objects.get(level=skillLevel)
    except:
        return None


def save_method(methods: list[str], recipe: Recipe):
    for index, method_string in enumerate(methods):
        Method.objects.create(recipe=recipe,
                              text=method_string,
                              step=index + 1)


def save_tags(tags: list[str]):
    tag_objects = []
    for tag_string in tags:
        tag, _ = Tag.objects.get_or_create(name=tag_string)
        tag_objects.append(tag)
    return tag_objects


def save_ingridients(ingridients: list[parsedIngridient], recipe: Recipe):
    for ingridient in ingridients:
        ing, _ = Ingredient.objects.get_or_create(name=ingridient.name,
                                                  externalId=0,
                                                  imageUrl='')
        RecipeIngredient.objects.get_or_create(
            recipe=recipe,
            ingredient=ing,
            quantity=ingridient.quantity,
            measurement=ingridient.measurement,
            text=ingridient.text,
        )


def save_recipe(data: ParsedRecipe):
    try:
        hasRecipe = Recipe.objects.filter(origUrl=data.sourceUrl).first()
        if hasRecipe:
            appendLog('has recipe', data.sourceUrl)
            return
        nutrition = save_nutrition(data.nutrition)
        tags = save_tags(data.tags)
        recipe = Recipe.objects.create(title=data.name,
                                       description="empty",
                                       dishNumber=data.dishNumber,
                                       preparationMinutes=data.time,
                                       nutrition=nutrition,
                                       skill_level=get_skillLevel(
                                           data.skillLevel),
                                       imageUrl=data.pictureUrl,
                                       origUrl=data.sourceUrl,
                                       source=data.source)
        recipe.tags.set(tags)
        recipe.save()
        save_method(data.method, recipe)
        save_ingridients(data.ingridients, recipe)

        return recipe
    except Exception as e:
        appendLog('save_recipe', e)
        return ''


def appendLog(place: str, string: str):
    with open('scrape_log.txt', 'a') as log_file:
        log_file.write(f'{place}:{string}\n')
