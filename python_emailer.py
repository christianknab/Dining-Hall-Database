import smtplib
import ssl
from email.message import EmailMessage
import sqlite3
import datetime

conn = sqlite3.connect('menus.db')
curr = conn.cursor()

today = datetime.date.today()

data = curr.execute("SELECT date, name, meal, item FROM menu WHERE (item LIKE '%Hash%Brown%' OR item LIKE '%tater%') AND date >= ?", (today,))

string = ''
for row in data:
    i = 0
    for col in row:
        if i == 0:
            if col not in string:
                string += col
                string += '\n'
        else:
            string += col
        string += '\n'
        i += 1

print(string)

# email_sender = 'ucscmenuapp@gmail.com'
# email_password = 'zhubiwjiwzhktqct'
# email_receiver = 'christiantknab@gmail.com'

# subject = 'Hello World'
# body = """This email was sent using Python :)"""

# em = EmailMessage()
# em['From'] = email_sender
# em['To'] = email_receiver
# em['Subject'] = subject
# em.set_content(body)

# context = ssl.create_default_context()

# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#     smtp.login(email_sender, email_password)
#     smtp.sendmail(email_sender, email_receiver, em.as_string())