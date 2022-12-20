from bs4 import BeautifulSoup
import requests


def fetch_data_fromXML(todaysDate):
    r = requests.get('http://www.sksdb.hacettepe.edu.tr/YemekListesi.xml')
    r.encoding = 'utf-8'
    xml_text = r.text

    soup = BeautifulSoup(xml_text, 'xml')

    meals = []
    calorie = 0
    for day in soup.select('gun'):
        date = day.select_one('tarih').text.split()[0]

        if date == todaysDate:
            for meal in day.select('yemek'):
                meal = meal.text.strip()

                if meal:
                    meals.append(meal)

            calorie = day.select_one('kalori').text

    if not meals:
        # Maybe introduce proper error handling with logging?
        print(f"[ERROR] There isn't a menu for the given date: {todaysDate}")

    return meals, calorie
