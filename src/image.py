"""
        Coordinates generally have been hard-coded. Make sure you tweak them,
        if you have different sized layers.
"""

import os
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont

from .config import BACKGROUND_COLORS


def generate_image(date: str, meals: list[str], calorie: str) -> BytesIO:
    magical_number = int(date.split('.')[0]) % len(BACKGROUND_COLORS)
    img = get_background(magical_number)
    paste(img)
    draw(img, meals, calorie)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer


def draw(background: Image.Image, meals: list[str], calorie: str) -> None:
    # Fonts
    default_font = ImageFont.truetype("resources/font/UbuntuCondensed-Regular.ttf", 50)
    title_font = ImageFont.truetype("resources/font/Courgette-Regular.ttf", 60)

    # Colors
    black_color = "#000000"
    blue_color = "#0000FF"
    red_color = "#FF0000"

    draw_ = ImageDraw.Draw(background)
    title = '~Günün Menüsü~'
    draw_.text((375, 50), title, font=title_font, fill=blue_color)
    increment_between_lines: float = 875 / len(meals)
    y = 220

    for meal in meals:
        draw_.text((75, y), text='• ' + meal, font=default_font, fill=black_color)
        y += increment_between_lines
    draw_.text((75, 1130), text=f'Toplam: {calorie} cal', font=default_font, fill=red_color)


def paste(background: Image.Image) -> None:
    icons = get_icons()
    locations = [(800, 40), (800, 800), (100, 1300), (600, 1300)]
    for i in range(len(icons)):
        background.paste(icons[i], locations[i], icons[i])


def get_background(i: int) -> Image.Image:
    size = (1200, 1600)
    color = BACKGROUND_COLORS[i]
    img = Image.new('RGB', size, color)
    return img


def get_icons() -> list[Image.Image]:
    square_path = "resources/icon/square/"
    nonsquare_path = "resources/icon/non-square/"
    icons = []
    r = (400, 400)
    k = (488, 300)

    squares_dir: list[str] = random.sample(os.listdir(square_path), 2)
    nonsquares_dir: list[str] = random.sample(os.listdir(nonsquare_path), 2)
    squares: list[Image.Image] = [Image.open(square_path + icon).resize(r) for icon in squares_dir]
    nonsquares: list[Image.Image] = [Image.open(nonsquare_path + icon).resize(k) for icon in nonsquares_dir]

    icons.extend(squares)
    icons.extend(nonsquares)
    return icons
