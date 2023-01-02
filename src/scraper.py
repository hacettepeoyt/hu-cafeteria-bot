from bs4 import BeautifulSoup, element
import requests


def fetch_data_fromXML(todaysDate: str) -> tuple[list[str], str]:
    r: requests.Response = requests.get(
        'http://www.sksdb.hacettepe.edu.tr/YemekListesi.xml')
    r.encoding = 'utf-8'
    xml_text: str = r.text

    soup: BeautifulSoup = BeautifulSoup(xml_text, 'xml')

    meals: list[str] = []
    calorie: str = ''

    day: element.Tag
    for day in soup.select('gun'):
        date: str = day.select_one('tarih').text.split()[0]

        if date == todaysDate:
            meal_tag: element.Tag
            for meal_tag in day.select('yemek'):
                meal_str: str = meal_tag.text.strip()

                if meal_str:
                    meals.append(meal_str)

            calorie = day.select_one('kalori').text

    if not meals:
        # Maybe introduce proper error handling with logging?
        print(f"[ERROR] There isn't a menu for the given date: {todaysDate}")

    return meals, calorie
