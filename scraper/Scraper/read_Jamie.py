#remmember to thank jamie olivers team,
#this is the site map: https://www.jamieoliver.com/recipes.xml

import re
import requests
from bs4 import BeautifulSoup

from scraper.Scraper.types.ingridient import parsedIngridient
from scraper.Utils.measurement_format import formatMeasurement
from ..Utils.types.nutrition_empty import Nutrition
from ..Utils.numbers import number_replacer
from ..Utils.measurementSet import measurementList, measurement_dictionary
from ..Utils.foodItemSet import foodItemList
from .types.scraper_types import ParsedRecipe, ScrapedRecipe
from .scraper_class import Recipe_Scraper
from ..Utils.util_types import Measurement

skillLevelDictionary = {'Super easy': 1, 'Not Too Tricky': 2, 'Showing off': 4}

word_pattern = r'\b(?:' + '|'.join(re.escape(item)
                                   for item in foodItemList) + r')\b'
units_pattern = r'|'.join(
    re.escape(unit) for unit in measurement_dictionary.keys())
measurement_pattern = rf'(\d+\.?\d*|\d+/\d+|\u00BD|\u00BE|\u00BC|\u2153|\u2154|\u2155|\u2156|\u2157)\s*({units_pattern})?\b'
# rf'(\d+\.?\d*|\d+/\d+|\u00BD|\u00BE|\u00BC|\u2153|\u2154|\u2155|\u2156|\u2157)\s*(?:a\s+)?({units_pattern})?'


class JamieScraper(Recipe_Scraper):

    def __init__(self) -> None:
        recipeMap = "https://www.jamieoliver.com/sitemap.xml"
        page = requests.get(recipeMap)
        soup = BeautifulSoup(page.content, "html.parser")
        try:
            self.urlList = [x.get_text() for x in soup.find_all('loc')]
            self.urlList = [
                x for x in self.urlList if x.find('/recipes/') > -1
            ]
        except:
            print("nana")

    def read_jamie(self, url: str) -> ScrapedRecipe:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        name = soup.find("h1"
                         # ,{"class": "type-h2 pt-24 sm:pt-32 astro-sntov27e"}
                         ).get_text()
        try:
            ingridients = [
                x.get_text()
                for x in soup.find("div", {
                    "class": "ingredients-rich-text"
                }).find_all("p")
            ]
        except Exception as e:
            # appendLog('read_jamie', 'failed to parse ingridients')
            raise Exception('failed to parse ingridients')

        try:
            method = [
                x.get_text() for x in soup.find_all(
                    "div", {"class": "recipe-page--method"})[0].find_all("li")
            ]
        except:
            appendLog('read_jamie', 'failed to parse method')
            raise Exception('failed to parse method')
        try:
            tags = [
                x.get_text() for x in soup.find_all(
                    "a", {"data-event-label": "recipes_pdp_tags_click"})
            ]
        except:
            appendLog('read_jamie', 'failed to parse tags')
            raise Exception('failed to parse tags')

        time, dishNumber, skillLevel = getRecipeFacts(soup)

        try:
            nutrition = getNutrition(soup)
        except:
            appendLog('read_jamie', 'failed to nutrition')
            raise Exception('failed to parse nutrition')

        pictureUrl = soup.find(
            "img", {
                "class": re.compile(r'media.*recipe-page__image')
            }).attrs['src']

        return ScrapedRecipe(name, method, ingridients, tags, time, dishNumber,
                             skillLevel, nutrition, pictureUrl)

    def _parse_name(self, jamieRecepie: ScrapedRecipe):
        return jamieRecepie.name

    def _parse_method(self, jamieRecepie: ScrapedRecipe):
        return jamieRecepie.method

    def _seperate_ingridients(self, input_string: str):
        input_string = input_string.lower()
        try:
            name = getIngridientName(input_string)
            if (name == ''):
                appendLog('parseIngridient name: ', input_string)
                return
            cleaned_text = re.sub(word_pattern,
                                  '',
                                  input_string,
                                  flags=re.IGNORECASE)
            measurements = getIngridientMeasurements(cleaned_text)
            if (measurements == ''):
                appendLog('parseIngridient measurement: ', input_string)
                return
            cleaned_text = re.sub(measurement_pattern,
                                  '',
                                  input_string,
                                  flags=re.IGNORECASE)

            if measurements:
                cleaned_text = re.sub(re.escape(name),
                                      '',
                                      cleaned_text,
                                      flags=re.IGNORECASE)

            # Get the remaining words
            remaining_words = cleaned_text.split()
            quantity, measurement = formatMeasurement(measurements['num'],
                                                      measurements['measur'])
            prsdIngridient = parsedIngridient(name, quantity, measurement,
                                              remaining_words)

            return prsdIngridient
        except Exception as e:
            appendLog('parseIngridient', 'parsing failed: ' + input_string)
            return

    def _parse_ingridients(
            self, jamieRecepie: ScrapedRecipe) -> list[parsedIngridient]:
        ingridients: list[parsedIngridient] = [
            self._seperate_ingridients(x) for x in jamieRecepie.ingridients
        ]
        ingridients = [x for x in ingridients if x]
        return ingridients

    def _parse_tags(self, jamieRecepie: ScrapedRecipe):
        try:
            return [x.lower() for x in jamieRecepie.tags]
        except:
            appendLog('parseTag', jamieRecepie.tags)

    def _parse_time(self, jamieRecepie: ScrapedRecipe) -> int:
        timeWordSet = {'min', 'minute', 'hour', 'hr'}
        time_pattern = rf'(\d+\.?\d*|\d+/\d+|\u00BD|\u00BE|\u00BC|\u2153|\u2154|\u2155|\u2156|\u2157)\s*({timeWordSet})?'
        word_match = re.findall(time_pattern, jamieRecepie.time, re.IGNORECASE)
        if word_match:
            return int(word_match[0][0]) if len(
                word_match[0]) == 1 else int(word_match[0][0]) * 60 + int(
                    word_match[1][0])
        else:
            appendLog('parseTime', time_pattern)
        return 0

    def _parse_dishNumber(self, jamieRecepie: ScrapedRecipe):
        try:
            dish_pattern = r'(\d+)'
            match = re.search(dish_pattern, jamieRecepie.dishNumber,
                              re.IGNORECASE)
            if match:
                number = match.group(1)
                return int(number)
            return 0
        except:
            appendLog('parseDishNumber', jamieRecepie.dishNumber)

    def _parse_skillLevel(self, jamieRecepie: ScrapedRecipe):
        return skillLevelDictionary.get(jamieRecepie.skillLevel, -1)

    def _parse_nutrition(self, jamieRecepie: ScrapedRecipe) -> Nutrition:
        try:
            nutrition: Nutrition = Nutrition(
                jamieRecepie.nutrition.get('Calories', 0),
                jamieRecepie.nutrition.get('Protein', 0),
                jamieRecepie.nutrition.get('Carbs', 0),
                jamieRecepie.nutrition.get('Fat', 0),
                jamieRecepie.nutrition.get('Saturates', 0),
                jamieRecepie.nutrition.get('Salt', 0),
                jamieRecepie.nutrition.get('Fiberalt', 0),
            )
            return nutrition
        except Exception as e:
            appendLog('parseNutrition', jamieRecepie.nutrition)

    def _parse_jamie_recipe(self, jamieRecepie: ScrapedRecipe, url: str):
        return ParsedRecipe(self._parse_name(jamieRecepie),
                            self._parse_method(jamieRecepie),
                            self._parse_ingridients(jamieRecepie),
                            self._parse_tags(jamieRecepie),
                            self._parse_time(jamieRecepie),
                            self._parse_dishNumber(jamieRecepie),
                            self._parse_skillLevel(jamieRecepie),
                            self._parse_nutrition(jamieRecepie), "jamie", url,
                            jamieRecepie.pictureUrl)

    def get_formatted_recipes(self):
        getUrls: list[str] = self.urlList
        recipes = [self.get_formatted_recipe(url) for url in getUrls]
        return recipes

    def getUrlList(self):
        return self.urlList

    def get_formatted_recipe(self, url: str):
        try:
            jamieRecepie: ScrapedRecipe = self.read_jamie(url)
            parsedRecipe = self._parse_jamie_recipe(jamieRecepie, url)
            # appendLog('format recipe succedded:', url)
            return parsedRecipe
        except Exception as e:
            # appendLog('format recipe failed: ' + e.args[0], url)
            pass

    def test_ingridient_parse(self):
        jamieRecepie: ScrapedRecipe = ScrapedRecipe('', '', [], [], '', '', '',
                                                    [])
        jamieRecepie.ingridients = [
            '500g higher-welfare pork belly slices', 'olive oil',
            '1 red pepper', '3 nests of flat rice noodles',
            '1 bunch of mint (30g)', '1 carrot', '1 bunch spring onions',
            '100g sugar snap peas', '1 tablespoon sesame seeds',
            '4cm piece of ginger', '½ a clove of garlic', '½ a red chilli',
            '1 tablespoon soy sauce', '1 teaspoon sesame oil',
            '1 teaspoon fish sauce'
        ]
        ingridients = self._parse_ingridients(jamieRecepie)

        expected = [('pork belly', 500, 'g'), ('olive oil', 0, ''),
                    ('red pepper', 1, ''), ('rice noodles', 3, 'nests'),
                    ('mint', 30, 'g'), ('carrot', 1, ''),
                    ('spring onions', 1, ''), ('sugar snap peas', 100, 'g'),
                    ('sesame seeds', 1, 'tablespoon'), ('ginger', 4, 'cm'),
                    ('garlic', 0.5, 'clove'), ('red chilli', 0.5, ''),
                    ('soy sauce', 1, 'tablespoon'),
                    ('sesame oil', 1, 'teaspoon'),
                    ('fish sauce', 1, 'teaspoon')]

        print('ans', 'expeted')
        for i, ingiridient in enumerate(ingridients):
            if ingiridient[0] != expected[i][0] or ingiridient[1] != expected[
                    i][1] or ingiridient[2] != expected[i][2]:
                print((ingiridient[0], expected[i][0]),
                      (ingiridient[1], expected[i][1])
                      if ingiridient[1] != expected[i][1] else '',
                      (ingiridient[2], expected[i][2])
                      if ingiridient[2] != expected[i][2] else '')


def getRecipeFacts(soup) -> tuple:
    recipeFacts = soup.find_all(
        "div", {"class": "recipe-facts__container"})[0].find_all("h6")

    time = recipeFacts[0].get_text()
    dishNumber = recipeFacts[2].get_text()
    skillLevel = recipeFacts[1].get_text()
    return time, dishNumber, skillLevel


def getNutrition(soup) -> list[tuple]:
    nutrition = soup.find_all("div",
                              {"class": "nutrition--card astro-oujdv6rb"})
    nutritionNames = [x.find("p").get_text() for x in nutrition]
    nutritionNumber = [x.find("span").get_text() for x in nutrition]
    nutrition = [(nutritionNames[i], nutritionNumber[i])
                 for i in range(0, len(nutritionNames))]
    nutrition = {x[0]: extractFloat(x[1]) for x in nutrition}
    if not set([
            'Calories', 'Protein', 'Carbs', 'Fat', 'Saturates', 'Salt', 'Fiber'
    ]).issubset(nutrition.keys()):
        appendLog('getNutrioton', nutrition)
    return nutrition


def getIngridientName(input_string):
    word_match = re.findall(word_pattern, input_string)
    name = '' if len(word_match) == 0 else max(word_match, key=len)
    return name


def getIngridientMeasurements(input_string):
    found_measurements = re.findall(measurement_pattern, input_string,
                                    re.IGNORECASE)
    measurements = [{
        'num': number_replacer(num),
        'measur': measur
    } for num, measur in found_measurements]
    nonEmptyMeasurememnt = [x for x in measurements if x['measur'] != '']
    if len(nonEmptyMeasurememnt) > 1:
        measurements = nonEmptyMeasurememnt[0]
    elif len(measurements) == 1:
        measurements = measurements[0]
    else:
        measurements = {'num': 1, 'measur': ''}
    return measurements


# JamieScraper().get_formatted_recipes()


def extractFloat(s: str) -> float:
    match = re.search(r'\d+\.?\d*', s)
    if match:
        return float(match.group(0))
    return 0.0


def appendLog(place: str, string: str):
    with open('scrape_log.txt', 'a') as log_file:
        log_file.write(f'{place}:{string}\n')
