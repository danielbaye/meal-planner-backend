import requests


def translateEnToHeb(string: str) -> str:
    try:
        obj = {
            'q': string,
            'source': "en",
            'target': "he",
            'format': "text",
            'alternatives': 3,
        }
        req = requests.post("http://localhost:5000/translate", obj)
        if req.status_code == 200:
            return req.json()['translatedText']
        return ''
    except Exception as e:
        print(e)
    return ''
