import os
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


class MenuImageGenerator:
    """
    Generates a menu image with a title, bullet pointed list of meals,
           and total calorie count.

    Args:
        background_colors (list[str], optional): A list of background colors
            for the menu image. Defaults to ["#FFFFFF"].
        title_font_path (str, optional): Path to the font file for the title.
            Defaults to "resources/font/Courgette-Regular.ttf".
        content_font_path (str, optional): Path to the font file for the meals
            and calorie content. Defaults to
            "resources/font/UbuntuCondensed-Regular.ttf".
        square_icon_path (str, optional): Path to the directory containing
            square menu icons. Defaults to "resources/icon/square".
        non_square_icon_path (str, optional): Path to the directory containing
            non-square menu icons. Defaults to "resources/icon/non-square".
        icon_sizes (dict, optional): A dictionary containing sizes for square
            and non-square icons. Defaults to {"square": (400, 400),
            "non_square": (488, 300)}.
        icon_locations (list[tuple[int]], optional): A list of tuples specifying
            the (x, y) coordinates for placing icons on the menu image. Defaults to
            [(800, 40), (800, 800), (100, 1300), (600, 1300)].
        title (str, optional): The title of the menu. Defaults to "Günün Menüsü"
            (Turkish for "Today's Menu").
        bullet_point (str, optional): The bullet point symbol to use before each
            meal item. Defaults to "•".
    """

    def __init__(
            self,
            background_colors: list[str] = None,
            title_font_path: str = "resources/font/Courgette-Regular.ttf",
            content_font_path: str = "resources/font/UbuntuCondensed-Regular.ttf",
            square_icon_path: str = "resources/icon/square",
            non_square_icon_path: str = "resources/icon/non-square",
            icon_sizes: dict = None,
            icon_locations: list[tuple[int]] = None,
            title: str = "Günün Menüsü",
            bullet_point: str = "•"
    ):
        if background_colors is None:
            background_colors = ["#FFFFFF"]

        if icon_sizes is None:
            icon_sizes = {
                "square": (400, 400),
                "non_square": (488, 300)
            }

        if icon_locations is None:
            icon_locations = [(800, 40), (800, 800), (100, 1300), (600, 1300)]

        self.background_colors = background_colors
        self.icon_sizes = icon_sizes
        self.title_font = ImageFont.truetype(title_font_path, size=60)
        self.content_font = ImageFont.truetype(content_font_path, size=50)
        self.square_icons = [os.path.join(square_icon_path, icon) for icon in os.listdir(square_icon_path)]
        self.non_square_icons = [os.path.join(non_square_icon_path, icon) for icon in os.listdir(non_square_icon_path)]
        self.icon_locations = icon_locations
        self.title = title
        self.bullet_point = bullet_point

        # Constants
        self.black_color = "#000000"
        self.blue_color = "#0000FF"
        self.red_color = "#FF0000"

    def generate(self, date: str, meals: list[str], calorie: str) -> BytesIO:
        """
        Generates a menu image with the provided date, meals, and calorie count.

        Args:
            date (str): The date for the menu.
            meals (list[str]): A list of meal items to be displayed on the menu.
            calorie (str): The total calorie count for the menu.

        Returns:
            BytesIO: A BytesIO object containing the generated image in PNG format.
        """
        magical_number = int(date.split(".")[0]) % len(self.background_colors)
        img = self._get_background(magical_number)
        self._paste_icons(img)
        self._draw_text(img, meals, calorie)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer

    def _draw_text(self, background: Image.Image, meals: list[str], calorie: str) -> None:
        """
        Draws the text elements on the menu image.

        Args:
            background (Image.Image): The background image to draw on.
            meals (list[str]): A list of meal items to be drawn.
            calorie (str): The total calorie count to be drawn.
        """
        draw_ = ImageDraw.Draw(background)
        draw_.text((375, 50), self.title, font=self.title_font, fill=self.blue_color)
        increment_between_lines = 875 / len(meals)
        y = 220

        for meal in meals:
            draw_.text((75, y), text=f"{self.bullet_point} {meal}", font=self.content_font, fill=self.black_color)
            y += increment_between_lines

        draw_.text((75, 1130), text=f"Toplam: {calorie} kalori", font=self.content_font, fill=self.red_color)

    def _paste_icons(self, background: Image.Image) -> None:
        """
        Pastes randomly selected icons onto the menu image.

        Args:
            background (Image.Image): The background image to paste icons on.
        """
        icons = self._get_icons()

        for i, icon in enumerate(icons):
            background.paste(icon, self.icon_locations[i], icon)

    def _get_background(self, i: int) -> Image.Image:
        """
        Creates a new background image with the specified color.

        Args:
            i (int): The index of the background color to use.

        Returns:
            Image.Image: The created background image.
        """
        size = (1200, 1600)
        color = self.background_colors[i]
        img = Image.new("RGB", size, color)
        return img

    def _get_icons(self) -> list[Image.Image]:
        """
        Selects four random icons, two square and two non-square, and loads them as images.

        Returns:
            list[Image.Image]: A list of four loaded icon images.
        """
        icons = []
        random_square_icons = random.sample(self.square_icons, 2)
        random_non_square_icons = random.sample(self.non_square_icons, 2)

        for icon in random_square_icons:
            icons.append(Image.open(icon).resize(self.icon_sizes["square"]))

        for icon in random_non_square_icons:
            icons.append(Image.open(icon).resize(self.icon_sizes["non_square"]))

        return icons
