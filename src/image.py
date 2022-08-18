'''
        Coordinates generally have been hard-coded. Make sure you tweak them,
        if you have different sized layers.
'''



import os
import random
import datetime

from PIL import Image, ImageDraw, ImageFont
from scraper import fetch_data_fromXML



### Background Colors ###
colors = ['#C9D6DF', '#F8F3D4', '#FFE2E2', '#E7D4B5',
          '#AEDEFC', '#EAFFD0', '#FFD3B4', '#BAC7A7',
          '#95E1D3', '#FCE38A', '#8785A2', '#F38181',
          '#FFB4B4']

### Fonts ###
default_font = ImageFont.truetype('resources/font/UbuntuCondensed-Regular.ttf', 50)
title_font = ImageFont.truetype('resources/font/Courgette-Regular.ttf', 60)

### Icon paths by type ###
square_path = 'resources/icon/square/'
nonsquare_path = 'resources/icon/non-square/'

### Generic RGB colors for fonts ###
black_color = (0,0,0)
blue_color = (0,7,166)
red_color = (255,17,0)




def main(todays_date):
    meals, calorie = fetch_data_fromXML(todays_date)

    today = datetime.date.today().day
    day = today % 13                        # There are 13 different background color, that's why.

    img = get_background(day)
    paste(img)
    draw(img, meals, calorie)
    img.save('menu.png')


def draw(background, meals, calorie):
    title = '~Günün Menüsü~'
    draw = ImageDraw.Draw(background)

    draw.text((375, 50), title, font=title_font, fill=blue_color)

    increment_between_lines = 875 / len(meals)

    y = 220
    for meal in meals:
        draw.text((75, y), text='• '+meal, font=default_font, fill=black_color)
        y += increment_between_lines

    draw.text((75,1130), text=f'Toplam: {calorie} cal', font=default_font, fill=red_color)


def paste(background):
    icons = get_icons()
    locations = [(800, 40), (800, 800), (100, 1300), (600, 1300)]

    for i in range(len(icons)):
        background.paste(icons[i], locations[i], icons[i])


def get_background(i):
    size = (1200, 1600)
    color = colors[i]
    img = Image.new('RGB', size, color)
    
    return img


def get_icons():
    icons = []
    r = (400, 400)
    k = (488, 300)

    squares = random.sample(os.listdir(square_path), 2)
    nonsquares = random.sample(os.listdir(nonsquare_path), 2)
    squares = [Image.open(square_path + icon).resize(r) for icon in squares]
    nonsquares = [Image.open(nonsquare_path + icon).resize(k) for icon in nonsquares]

    icons.extend(squares)
    icons.extend(nonsquares)

    return icons

