import re
from api.models.ingridient import Ingredient
from api.models.nutrition import Nutrition
from scraper.Utils.translate import translateEnToHeb
from bs4 import BeautifulSoup
import requests


def findIngridientHebName(ingridient_name: str) -> str:
    return translateEnToHeb(ingridient_name)


def findIngridientAverageCost(ingridient_id: str) -> float:
    if ingridient_id == '0' or not check_hebrew_or_integer(ingridient_id):
        return 0
    try:
        url = f'https://chp.co.il/חיפה/0/0/{ingridient_id}'
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        td = soup.findAll("td")
        h3 = soup.findAll("h3")
        gram_pattern = re.compile(r'(\d+\.?\d*)\s*(ג|גרם)')
        text = '' if h3[1] is None else h3[1].get_text()
        match = gram_pattern.search(text)
        total = 1
        if match:
            # Extract the number from the match
            grams = float(match.group(1))
            total = grams / 100
        try:
            text_td = [
                float(x.get_text()) for x in td
                if re.match(r'^-?\d+(?:\.\d+)$', x.get_text()) is not None
            ]
            return sum(text_td) / len(text_td) / total
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)
    return 0


def findIngridientImageUrl(ingridient_name: str) -> str:
    try:
        APP_ID = 658057
        ACCESS_KEY = 'dVsQ5xHNs2f-IzA-DIsvydLDrY1wYbge8IW9xUqLJvs'
        SECRET_KEY = '6PxiRiFwX5twyhzIYf5rUREpmUnp1nh_SiSuKSyqhK8'
        url = f'https://www.pexels.com/search/{ingridient_name}/'
        headers = {
            'sec-ch-ua-platform':
            "Windows",
            'sec-ch-ua':
            '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
        }
        page = requests.get(url, headers=headers, allow_redirects=True)
        soup = BeautifulSoup(page.content, "html.parser")
        imageUrl = soup.find("img").attrs['src']
        if imageUrl:
            return imageUrl
    except Exception as e:
        return ''
    return ''


def findIngridientNutrition(ingridient_name: str) -> Nutrition:
    pass


def parseIngridient(ingridient: Ingredient) -> bool:
    try:
        heb_name = ingridient.heb_name if ingridient.heb_name else findIngridientHebName(
            ingridient.name)
        imageUrl = ''  #findIngridientImageUrl(ingridient.name)
        cost = 0 if len(heb_name) == 0 else findIngridientAverageCost(
            ingridient.externalId if ingridient.externalId !=
            '0' else heb_name)
        #nutrition
        ingridient.cost_per_100_gr_ml = cost
        ingridient.imageUrl = imageUrl
        ingridient.heb_name = heb_name
        ingridient.save()
        return True
    except Exception as e:
        print(e)
    return False


def check_hebrew_or_integer(value):
    return value if (value.isdigit() and int(value) > 0) or re.search(
        r'[\u0590-\u05FF]', value) else None
