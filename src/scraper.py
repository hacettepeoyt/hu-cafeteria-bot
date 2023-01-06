from bs4 import BeautifulSoup, element, Tag
import requests
from typing import Optional


def fetch_data_fromXML(todaysDate: str) -> tuple[list[str], str]:
    possible_dates: list[str] = find_possible_dates(todaysDate)

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

        if date in possible_dates:
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