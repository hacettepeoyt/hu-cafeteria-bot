import requests


def get_iftarVakti_today():
    r = requests.get('https://namaz-vakti-api.herokuapp.com/data?region=9206')
    prayer_times = r.json()
    todays_iftar_time = prayer_times[0][5].replace(':', '.')

    return todays_iftar_time