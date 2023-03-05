import csv
import sqlite3

conn = sqlite3.connect("menus.db")

cursor = conn.cursor()
cursor.execute("select * from menu;")
with open("out.csv", "w", newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description]) # write headers
    csv_writer.writerows(cursor)
