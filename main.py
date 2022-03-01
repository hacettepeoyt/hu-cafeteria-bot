from bs4 import BeautifulSoup
import requests
import pandas as pd


# Renaming file names in order to sort them automatically.
def dateReverser(date):
    tempList = date.split(".")
    newDate = f"{tempList[2]}.{tempList[1]}.{tempList[0]}"
    return newDate


# There are more than one function to fetch the data from website.
# One of them uses classic HTML parsing, other one uses XML parsing.
# I'm using XML fetcher because it's more understandable and clean.
# But I'm keeping both of the functions in case one makes a problem.


def fetch_data_fromXML():
    r = requests.get('http://www.sksdb.hacettepe.edu.tr/YemekListesi.xml')
    r.encoding = 'utf-8'
    xml_text = r.text

    soup = BeautifulSoup(xml_text, 'xml')


    dates = []
    meals = []
    calories = []
    for day in soup.select('gun'):
        dailyMeal = []
        date = day.select_one('tarih').text.split()[0]
        dates.append(dateReverser(date))

        for meal in day.select('yemek'):
            dailyMeal.append(meal.text.strip())

        calorie = day.select_one('kalori').text
        calories.append(calorie)
        meals.append(dailyMeal)

    menu_df = pd.DataFrame(list(zip(dates, meals, calories)),
                           columns=['dates', 'meals', 'calories'])

    menu_df.to_csv('hacettepe_menu.csv')





def fetch_data_fromURL():
    r = requests.get('http://www.sksdb.hacettepe.edu.tr/bidbnew/grid.php?parameters=qbapuL6kmaScnHaup8DEm1B8maqtur'
                     'W8haidnI%2Bsq8F%2FgY1fiZWdnKShq8bTlaOZXq%2BmwWjLzJyPlpmcpbm1kNORopmYXI22tLzHXKmVnZykwafFhImVn'
                     'ZWipbq0f8qRnJ%2BioF6go7%2FOoplWqKSltLa805yVj5agnsGmkNORopmYXam2qbi%2Bo5mqlXRrinJdf1BQUFBXWXVMc39QUA%3D%3D')

    r.encoding = 'utf-8'
    html_text = r.text

    soup = BeautifulSoup(html_text, 'lxml')
    complexData = soup.find_all(class_="pricing")
    # print(complexData)

    for dailyComplexData in complexData:
        temp = dailyComplexData.get_text(separator='\n').split('\n')
        date, weekday = temp[0].split()[1], temp[0].split()[2]
        # print(temp)

        preMenu = []
        calorie = None
        for i in range(4, len(temp)):
            meal = temp[i].strip()

            if meal == "Kalori :":
                calorie = temp[i + 1]
                break

            preMenu.append(meal)

        # Identification of 'Sıhhiye' and 'Beytepe' strings.
        # There are two different campus of Hacettepe University, therefore we should be aware of this situation.
        menu = []
        j = 0
        while j < len(preMenu):

            if preMenu[j] == "Sıhhiye":
                myStr = f"Sıhhiye - {preMenu[j + 1]}"
                menu.append(myStr)
                j += 1
            elif preMenu[j] == "Beytepe":
                myStr = f"Beytepe - {preMenu[j + 1]}"
                menu.append(myStr)
                j += 1
            else:
                menu.append(preMenu[j])

            j += 1

        with open(f'dailyMenus/{dateReverser(date)}', 'w') as f:
            for meal in menu:
                f.writelines(f"{meal}\n")

            f.writelines(f"\nKalori: {calorie}")


fetch_data_fromXML()
