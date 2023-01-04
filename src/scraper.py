from bs4 import BeautifulSoup, element, Tag
import requests
from typing import Optional


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
        day_date_obj: Optional[Tag] = day.select_one('tarih')
        assert day_date_obj is not None, "[ERROR] Can't get the date from the XML."
        date: str = day_date_obj.text.split()[0]

        if date == todaysDate:
            meal_tag: element.Tag
            for meal_tag in day.select('yemek'):
                meal_str: str = meal_tag.text.strip()

                if meal_str:
                    meals.append(meal_str)
            calorie_select_obj: Optional[Tag] = day.select_one('kalori')
            assert calorie_select_obj is not None, "[ERROR] Can't get total calorie amount from the XML."
            calorie = calorie_select_obj.text

    if not meals:
        # Maybe introduce proper error handling with logging?
        print(f"[ERROR] There isn't a menu for the given date: {todaysDate}")

    return meals, calorie
