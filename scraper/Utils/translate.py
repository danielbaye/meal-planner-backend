import re
import requests
from bs4 import BeautifulSoup
import unicodedata


def translateEnToHeb(string: str) -> str:
    try:

        req = requests.get(f"https://www.morfix.co.il/{string}")
        soup = BeautifulSoup(req.content, "html.parser")
        found = soup.find("div",
                          {'class': 'MachineTranslation_divfootertop_enTohe'})
        if found:
            return unicodedata.normalize(
                'NFD',
                found.get_text().split(';')[0].split(',')[0].split('\n')[0])
        elif soup.find("div", {'class': 'wiki_to_he'}):
            return soup.find("div", {'class': 'wiki_to_he'}).get_text()

        else:
            found = soup.find_all("div",
                                  {'class': 'normal_translation_div'})[0]
            split = found.get_text().split(';')[0].split(',')[0].split('\n')
            split = split[0] if len(split[0]) > 2 else split[1]
            return unicodedata.normalize('NFD', split)

    except Exception as e:
        print(e)
    return ''
