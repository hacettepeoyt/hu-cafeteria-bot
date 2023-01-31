from bs4 import BeautifulSoup, element, Tag
import requests
from typing import Optional, Dict, List, Tuple


def fetch_data_fromXML() -> Dict[str, Tuple[List[str], str]]:
    r: requests.Response = requests.get('http://www.sksdb.hacettepe.edu.tr/YemekListesi.xml')
    r.encoding = 'utf-8'
    xml_text: str = r.text
    dictionary_for_matching = {}
    soup: BeautifulSoup = BeautifulSoup(xml_text, 'xml')

    meals: list[str] = []
    calorie: str = ''
    dates = []
    days = []
    calories = []
    day: element.Tag
    for day in soup.select('gun'):
        day_date_obj: Optional[Tag] = day.select_one('tarih')
        day_date_object = day.select_one('tarih')
        a = day_date_object.text.strip()
        current_date_and_day = a.split("<p>")[0]
        dates.append(current_date_and_day.split()[0])
        days.append(current_date_and_day.split()[1])

        meal_tag: element.Tag
        for meal_tag in day.select('yemekler'):
            meal_str: str = meal_tag.text.strip()

            if meal_str:
                meals.append(meal_str)
        calorie_select_obj: Optional[Tag] = day.select_one('kalori')
        assert calorie_select_obj is not None, "[ERROR] Can't get total calorie amount from the XML."
        calorie = calorie_select_obj.text
        calories.append(calorie)
    if not meals:
        # Maybe introduce proper error handling with logging?
        print(f"[ERROR] There isn't a menu in the XML: ")

    for i in range(len(meals)):
        meals[i] = [meals[i].split("\n")]
        dictionary_for_matching[dates[i]] = meals[i], calories[i]
    return dictionary_for_matching


def find_possible_dates(_date: str) -> list[str]:
    """
    A date can be represented in different formats. Such as, January 6th of 2023 can
    be written in 4 different way:
    1.  06.01.2023
    2.  6.01.2023
    3.  6.1.2023
    4.  06.1.2023

    Here I created a list that contains all of the possibilities. The website that is being
    scraped uses 6.01.2023, but they may not be decisive on this too (Remember the meal names).

    Note that, the _date value will be assumed in DD.YY.YYYY
    """

    split_date: list[str] = _date.split('.')
    day: str = split_date[0]
    month: str = split_date[1]
    year: str = split_date[2]

    possible_dates: list[str] = [_date]
    possible_dates.append(f'{int(day)}.{month}.{year}')
    possible_dates.append(f'{int(day)}.{int(month)}.{year}')
    possible_dates.append(f'{day}.{int(month)}.{year}')

    return possible_dates

