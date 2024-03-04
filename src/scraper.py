import xml.etree.ElementTree as ET

import aiohttp


async def scrape() -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get("http://www.sksdb.hacettepe.edu.tr/YemekListesi.xml") as resp:
            xml_text = await resp.text()
            return parse_menu(xml_text)


def parse_menu(xml_string):
    root = ET.fromstring(xml_string)
    menu_dict = {}
    for gun in root.findall('gun'):
        tarih = standardize_date(gun.find('tarih').text.split()[0])
        yemekler = [yemek.text.strip() for yemek in gun.find('yemekler').findall('yemek') if yemek.text.strip()]
        calorie = gun.find('kalori').text
        menu_dict[tarih] = {"meals": yemekler, "calorie": calorie}
    return menu_dict


def standardize_date(date_text: str) -> str:
    temp = date_text.split('.')
    day, month, year = temp[0], temp[1], temp[2]

    if len(day) == 1:
        day = '0' + day
    if len(month) == 1:
        month = '0' + month

    return day + '.' + month + '.' + year
