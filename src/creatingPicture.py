from PIL import Image, ImageDraw, ImageFont
import datetime
import fetchingMenu


def main(todaysDate):
    meals, calorie = fetchingMenu.fetch_data_fromXML(todaysDate)

    today = datetime.date.today().day
    day = today % 14                        # This will be used for choosing background image. There are 14 different images.

    # Color tuples
    blackColor = (0,0,0)
    redColor = (255,17,0)
    blueColor = (0,7,166)

    # Backround pictures
    pinkBackground = 'resources/backgrounds/pink.jpg'
    blueBackground = 'resources/backgrounds/blue.jpg'
    greenBackground = 'resources/backgrounds/green.jpg'
    yellowBackground = 'resources/backgrounds/yellow.jpg'
    lilacBackground = 'resources/backgrounds/lilac.jpg'
    purpleBackground = 'resources/backgrounds/purple.jpg'
    greyBackground = 'resources/backgrounds/grey.jpg'


    # This is for changing the color-background duo every 8 days.
    dailySets = ((pinkBackground, blueColor), (blueBackground, blueColor), (greenBackground, blueColor), (yellowBackground, blueColor),
                 (lilacBackground, blueColor), (purpleBackground, blueColor), (greyBackground, blueColor), (pinkBackground, blackColor),
                 (blueBackground, blackColor), (greenBackground, blackColor), (yellowBackground, blackColor), (lilacBackground, blackColor),
                 (purpleBackground, blackColor), (greyBackground, blackColor))

    # Choosing background image and font color
    todaysBackground = dailySets[day][0]
    todaysColor = dailySets[day][1]

    img = Image.open(todaysBackground)
    defaultFont = ImageFont.truetype('resources/fonts/UbuntuCondensed-Regular.ttf', 50)
    titleFont = ImageFont.truetype('resources/fonts/Courgette-Regular.ttf', 60)

    menu = ImageDraw.Draw(img)
    menu.text((315,50), '~Günün Menüsü~', font=titleFont, fill=todaysColor)

    increment_between_lines = 875 / len(meals)

    # One by one placing meals into the menu picture
    yCoordinate = 220
    for meal in meals:
        menu.text((75, yCoordinate), text='• '+meal, font=defaultFont, fill=todaysColor)
        yCoordinate += increment_between_lines

    menu.text((75,1130), text=f'Toplam: {calorie} cal', font=defaultFont, fill=redColor)

    img.save(f'menu.png')
