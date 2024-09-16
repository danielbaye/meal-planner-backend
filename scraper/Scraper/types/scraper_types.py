from scraper.Scraper.types.ingridient import parsedIngridient
from scraper.Utils.types.nutrition_empty import Nutrition
from scraper.Utils.util_types import Measurement


class ScrapedRecipe:
    name: str
    method: list[str]
    ingridients: list[str]
    tags: list[str]
    time: str
    dishNumber: str
    skillLevel: str
    nutrition: list[tuple[str, str]]
    pictureUrl: str

    def __init__(self, name: str, method: list[str], ingridients: list[str],
                 tags: list[str], time: str, dishNumber: str, skillLevel: str,
                 nutrition: list[tuple[str, str]], pictureUrl: str):
        self.name = name
        self.method = method
        self.ingridients = ingridients
        self.tags = tags
        self.time = time
        self.dishNumber = dishNumber
        self.skillLevel = skillLevel
        self.nutrition = nutrition
        self.pictureUrl = pictureUrl


class ParsedRecipe:
    name: str
    method: list[str]
    ingridients: list[parsedIngridient]
    tags: list[str]
    time: int
    dishNumber: int
    skillLevel: int
    nutrition: Nutrition
    source: str
    sourceUrl: str
    pictureUrl: str

    def __init__(self, name: str, method: list[str],
                 ingridients: list[parsedIngridient], tags: list[str],
                 time: int, dishNumber: int, skillLevel: int,
                 nutrition: Nutrition, source: str, sourceUrl: str,
                 pictureUrl: str):
        self.name = name
        self.method = method
        self.ingridients = ingridients
        self.tags = tags
        self.time = time
        self.dishNumber = dishNumber
        self.skillLevel = skillLevel
        self.nutrition = nutrition
        self.source = source
        self.sourceUrl = sourceUrl
        self.pictureUrl = pictureUrl
