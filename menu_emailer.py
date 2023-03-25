from playwright.sync_api import sync_playwright, ViewportSize
import re
import unicodedata
from bs4 import BeautifulSoup
from copy import deepcopy
# from datetime import datetime, timedelta
import datetime
import sqlite3
import time

def menu_scrape():
    url = 'https://nutrition.sa.ucsc.edu/'
    halls_html = ['text=College Nine/John R. Lewis Dining Hall', 'text=Cowell/Stevenson Dining Hall', 'text=Crown/Merrill Dining Hall', 'text=Porter/Kresge Dining Hall']
    dates = [str(datetime.date.today() + datetime.timedelta(days=i)) for i in range(7)]
    halls_name = ['Nine', 'Cowell', 'Merrill', 'Porter']
    meals = ["Breakfast", "Lunch", "Dinner", "Late Night"]
    food_cat = {"Breakfast": [], "Soups": [], "Entrees": [], "Grill": [], "Pizza": [], "Clean Plate": [], "Bakery": [], "Open Bars": [], "DH Baked": [], "Plant Based Station": [], "Miscellaneous": [], "Brunch": []}

    # Create nested dictionary
    meal_times = {}
    for i in meals:
        meal_times.update({i: deepcopy(food_cat)})

    meal_dates = {}
    for i in halls_name:
        meal_dates.update({i: deepcopy(meal_times)})

    hall_menus = {}
    for i in dates:
        hall_menus.update({i: deepcopy(meal_dates)})

    # Go through every dining hall college and update hall_menus dictionary
    for j in range(len(halls_name)):
        index = 0                                                       # reset index
        for date in dates:                                              # loop through dates wanted
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.set_viewport_size(ViewportSize(width = 1080*2, height=1920*2))
                page.goto(url)
                page.locator(halls_html[j]).click()                     # select hall
                date_option = page.get_by_role("combobox")              # find date options
                
                # find initial index of date options
                if index == 0:
                    options = date_option.locator("option").all_inner_texts()
                    for item in options:
                        # temp = str(datetime.date.today().strftime('%e'))
                        if str(datetime.date.today().strftime('%e')) in item:
                            index = options.index(item)                 # find index of current day's date
                            break
                date_option.select_option(index=index)                  # select day
                page.get_by_role("button", name="Go!").click()          # go to page
                index += 1

                html = page.content()
                soup = BeautifulSoup(html, 'html.parser')
                browser.close()

            menuTable = soup.find('table',  {'bordercolor': '#CCC'})    # Finds meal table

            if menuTable == None:                                       # Error check if hall is closed
                continue
            
            for meal in menuTable:                                      # For each item in the meal table, strip empty text
                text = meal.text.strip()                                # and save the menu item
                meal.string = re.sub(r"[\n][\W]+[^\w]", "\n", text)
                
            # Format List
            cleaned = unicodedata.normalize("NFKD", meal.text)          # Cleans html
            meals_list = []
            meals_list = cleaned.split("\n")                            # Splits data into a list
            for i in range(len(meals_list)):
                meals_list[i] = meals_list[i].strip()

            # Remove "nutrition calculator" from meals list
            n_calc_caount = meals_list.count('Nutrition Calculator')
            for i in range(n_calc_caount):
                meals_list.remove('Nutrition Calculator')

            # Updates hall_menu dictionary
            for i in meals_list:
                if i in meal_times.keys():                              # If Breakfast, Lunch, Dinner, or Late Night
                    meal_time = i                                       # Set current meal time
                    continue
                elif "--" in i:                                         # If at a meal category
                    meal_cat = i.strip("- ")                            # Clean string
                    meal_cat = meal_cat
                    continue
                else:                                                   # Append meals to dictionary
                    try:
                        hall_menus[date][halls_name[j]][meal_time][meal_cat].append(i)
                    except:
                        hall_menus[date][halls_name[j]][meal_time].update({meal_cat: []})
                        hall_menus[date][halls_name[j]][meal_time][meal_cat].append(i)

    return hall_menus

# main
hall_menus = menu_scrape()


conn = sqlite3.connect("menus.db")

# Create a new table in the database
conn.execute('''
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    name TEXT NOT NULL,
    meal TEXT NOT NULL,
    category TEXT NOT NULL,
    item TEXT NOT NULL
);
''')

startTime = time.time()
for date, names in hall_menus.items():
    for name, meals in names.items():
        for meal, cats in meals.items():
            for cat, items in cats.items():
                if len(items) > 0:
                    for item in items:
                        # date_obj = datetime.datetime.strptime(date, '%Y-%m-%d').date()
                        # write to database
                        # conn.execute('INSERT INTO menu (date, name, meal, category, item) VALUES (?, ?, ?, ?, ?) WHERE NOT EXISTS (SELECT 1 FROM menu WHERE date = ?)', (date, name, meal, cat, item))
                        cur = conn.cursor()
                        cur.execute('SELECT * FROM menu WHERE date=? AND name=? AND meal=? AND category=? AND item=?;', (date, name, meal, cat, item))
                        record = cur.fetchone()
                        if record:
                            # print("record already exists")
                            continue
                        else:
                            conn.execute('INSERT INTO menu (date, name, meal, category, item) VALUES (?, ?, ?, ?, ?);', (date, name, meal, cat, item))
                            # conn.execute('INSERT OR IGNORE INTO menu (date, name, meal, category, item) VALUES (?, ?, ?, ?, ?)', (date, name, meal, cat, item))

conn.commit()
conn.close()
# cur.close()