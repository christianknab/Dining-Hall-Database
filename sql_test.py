import sqlite3

conn = sqlite3.connect('menus.db')
curr = conn.cursor()

data = curr.execute('SELECT item FROM menu WHERE item LIKE "%Hash%Brown%"')

print(data.fetchall())