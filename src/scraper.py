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
                text = meal.text.strip()

                if '*' in text and text[0] != '*':
                    split = text.split('*')
                    meals.append(split[0])
                    meals.append('*' + split[1].strip())
                else:
                    meals.append(text)

            calorie = day.select_one('kalori').text

    return meals, calorie
    
