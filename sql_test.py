import sqlite3
import datetime

conn = sqlite3.connect('menus.db')
curr = conn.cursor()

today = datetime.date.today()
data = curr.execute("SELECT date, name, meal, item FROM menu WHERE (item LIKE '%Hash%Brown%' OR item LIKE '%tater%') AND date >= ?", (today,))

# print(data.fetchall())

for item in data:
    print(item)