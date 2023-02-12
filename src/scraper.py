from typing import Dict

import requests
from bs4 import BeautifulSoup


def scrape() -> Dict:
    r: requests.Response = requests.get("http://www.sksdb.hacettepe.edu.tr/YemekListesi.xml")
    r.encoding = "utf-8"
    xml_text: str = r.text
    soup: BeautifulSoup = BeautifulSoup(xml_text, "xml")
    all_menus = {}

    for day in soup.select("gun"):
        date = day.select_one("tarih").text.strip().split()[0]
        date = standardize_date(date)
        meal_list = []

        for yemek in day.select("yemek"):
            meal: str = yemek.text.strip()

            if meal:
                meal_list.append(meal)

        calorie = day.select_one("kalori").text.strip()
        menu = {"meals": meal_list, "calorie": calorie}
        all_menus[date] = menu

    return all_menus


def standardize_date(date_text: str) -> str:
    temp = date_text.split('.')
    day, month, year = temp[0], temp[1], temp[2]

    if len(day) == 1:
        day = '0' + day
    if len(month) == 1:
        month = '0' + month

    return day + '.' + month + '.' + year
