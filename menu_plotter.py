import matplotlib.pyplot as plt 
import pandas as pd
import sqlite3


conn = sqlite3.connect("menus.db")
# data = conn.execute("SELECT item, count(*) FROM menu WHERE category IN ('Open Bars', 'Entrees') AND item NOT LIKE '%rice%' AND ITEM NOT LIKE '%condiments%' GROUP BY item")
data = conn.execute("""
    SELECT name, count(*) FROM menu
    WHERE item LIKE '%Tater Tots%'
    OR item LIKE '%hash%'
    GROUP BY name
    ORDER BY count(*) DESC
""")
df = pd.DataFrame(data, columns=['item', 'count'])
plt.hist(df['item'], bins=len(df), weights=df['count'])
plt.xticks(rotation=90, fontsize=6)
plt.show()