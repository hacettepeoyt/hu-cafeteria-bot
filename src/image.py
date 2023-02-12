"""
        Coordinates generally have been hard-coded. Make sure you tweak them,
        if you have different sized layers.
"""

import os
import random

from PIL import Image, ImageDraw, ImageFont

# Background Colors
colors: list[str] = ['#C9D6DF', '#F8F3D4', '#FFE2E2', '#E7D4B5',
                     '#AEDEFC', '#EAFFD0', '#FFD3B4', '#BAC7A7',
                     '#95E1D3', '#FCE38A', '#8785A2', '#F38181',
                     '#FFB4B4']

# Fonts
default_font: ImageFont.FreeTypeFont = ImageFont.truetype('resources/font/UbuntuCondensed-Regular.ttf', 50)
title_font: ImageFont.FreeTypeFont = ImageFont.truetype('resources/font/Courgette-Regular.ttf', 60)

# Icon paths by type
square_path: str = 'resources/icon/square/'
nonsquare_path: str = 'resources/icon/non-square/'

# Generic RGB colors for fonts
black_color: tuple[int, int, int] = (0, 0, 0)
blue_color: tuple[int, int, int] = (0, 7, 166)
red_color: tuple[int, int, int] = (255, 17, 0)


def generate_image(date: str, meals: list[str], calorie: str) -> None:
    day: int = int(date.split('.')[0]) % len(colors)
    img: Image.Image = get_background(day)
    paste(img)
    draw(img, meals, calorie)
    img.save('menu.png')


def draw(background: Image.Image, meals: list[str], calorie: str) -> None:
    title: str = '~Günün Menüsü~'
    draw_: ImageDraw.ImageDraw = ImageDraw.Draw(background)
    draw_.text((375, 50), title, font=title_font, fill=blue_color)
    increment_between_lines: float = 875 / len(meals)
    y: int = 220

    for meal in meals:
        draw_.text((75, y), text='• ' + meal, font=default_font, fill=black_color)
        y += increment_between_lines

    draw_.text((75, 1130), text=f'Toplam: {calorie} cal', font=default_font, fill=red_color)


def paste(background: Image.Image) -> None:
    icons: list[Image.Image] = get_icons()
    locations: list[tuple[int, int]] = [(800, 40), (800, 800), (100, 1300), (600, 1300)]

    for i in range(len(icons)):
        background.paste(icons[i], locations[i], icons[i])


def get_background(i: int) -> Image.Image:
    size: tuple[int, int] = (1200, 1600)
    color: str = colors[i]
    img: Image.Image = Image.new('RGB', size, color)
    return img


def get_icons() -> list[Image.Image]:
    icons: list[Image.Image] = []
    r: tuple[int, int] = (400, 400)
    k: tuple[int, int] = (488, 300)

    squares_dir: list[str] = random.sample(os.listdir(square_path), 2)
    nonsquares_dir: list[str] = random.sample(os.listdir(nonsquare_path), 2)
    squares: list[Image.Image] = [Image.open(square_path + icon).resize(r) for icon in squares_dir]
    nonsquares: list[Image.Image] = [Image.open(nonsquare_path + icon).resize(k) for icon in nonsquares_dir]

    icons.extend(squares)
    icons.extend(nonsquares)
    return icons
