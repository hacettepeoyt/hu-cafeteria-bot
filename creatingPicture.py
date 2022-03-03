from PIL import Image, ImageDraw, ImageFont
import datetime
import pandas as pd


def main(todaysDate):

    # Reading the menu from csv file with pandas.
    hacettepe_menu = pd.read_csv('hacettepe_menu.csv', index_col='date')
    meals = str(hacettepe_menu.loc[todaysDate]['meal']).split('&&')
    calorie = str(hacettepe_menu.loc[todaysDate]['calorie'])

    today = datetime.date.today().day
    day = today % 14

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
    font = ImageFont.truetype('resources/fonts/UbuntuCondensed-Regular.ttf', 50)
    titeFont = ImageFont.truetype('resources/fonts/Courgette-Regular.ttf', 60)

    menu = ImageDraw.Draw(img)
    menu.text((315,50), '~Günün Menüsü~', font=titeFont, fill=todaysColor)

    # One by one placing meals into the menu picture
    y = 220
    for meal in meals:
        menu.text((75, y), text='• '+meal, font=font, fill=todaysColor)
        y += 150

    menu.text((75,1130), text=f'Toplam: {calorie} cal', font=font, fill=redColor)

    img.save(f"menu.png")
