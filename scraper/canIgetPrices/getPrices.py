from bs4 import BeautifulSoup
import requests
import os
import threading
import json

# url = f"https://url.publishedprices.co.il/file/json/dir"
# loginUrl = url + "login"


def download_file(url, name, dir_name):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        file_path = os.path.join(dir_name,
                                 f"{name}")  # Change .txt to desired file type
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded: {name} from {url}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")


def downloadGZ(url, download_url, dir_name):
    try:
        page = requests.get(url)
        list_of_contents = json.loads(page.content.decode('utf-8'))

        price_elements = [x['FileNm'] for x in list_of_contents]
        os.makedirs(dir_name, exist_ok=True)
        threads = []
        for name in price_elements:
            file_url = download_url + name
            thread = threading.Thread(target=download_file,
                                      args=(file_url, name, dir_name))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
    except Exception as e:
        print(f"Failed to read from url: {url}: {e}")


href_list = [
    'https://kingstore.binaprojects.com/',
    # 'http://maayan2000.binaprojects.com/',
    # 'https://goodpharm.binaprojects.com/',
    # 'http://zolvebegadol.binaprojects.com/',
    # 'https://supersapir.binaprojects.com/',
    # 'https://citymarketkiryatono.binaprojects.com/',
    # 'https://citymarketkiryatgat.binaprojects.com/',
    # 'https://citymarketgivatayim.binaprojects.com/',
    # 'http://superbareket.binaprojects.com/',
    # 'http://shuk-hayir.binaprojects.com/',
    # 'http://shefabirkathashem.binaprojects.com/',
    # 'http://paz.binaprojects.com/',
    # 'https://ktshivuk.binaprojects.com/',
]
for h in href_list:

    url = f"{h}MainIO_Hok.aspx?WStore=0&WDate=&WFileType=4"
    download_url = f"{h}Download/"
    dir_name = "goodfarm"
    downloadGZ(url, download_url, dir_name)

# page = requests.get(
#     'https://www.gov.il/ContentPageWebApi/api/content-pages/cpfta_prices_regulations?culture=he'
# )
# list_of_stuff = json.loads(page.content.decode('utf-8'))
# html_string = list_of_stuff['contentMain']['htmlContents'][0]['sectionData']
# soup = BeautifulSoup(html_string, 'html.parser')
# soup_table = soup.find('table')
# aa = soup_table.find_all('a')
# hrefs = [x['href'] for x in aa]
# for h in hrefs:
#     print(h)
