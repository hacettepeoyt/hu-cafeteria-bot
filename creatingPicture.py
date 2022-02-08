from PIL import Image, ImageDraw, ImageFont
import datetime


def main(txtFile):
    menuTxt = open(txtFile).readlines()

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
    calorie = None
    for line in menuTxt:
        line = line.replace('\n', '')
        if line == '':
            continue
        if line.split()[0] == 'Kalori:':
            calorie = line.split()[1]
            break

        menu.text((75, y), text='• '+line, font=font, fill=todaysColor)
        y += 150


    menu.text((75,1130), text=f'Toplam: {calorie} cal', font=font, fill=redColor)

    img.save('menu.png')
