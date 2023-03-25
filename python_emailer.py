import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from login_credentials import me_email, you_email, login_pass
import sqlite3
import datetime

conn = sqlite3.connect('menus.db')
curr = conn.cursor()

today = datetime.date.today()

data = curr.execute("SELECT date, name, meal, item FROM menu WHERE (item LIKE '%Hash%Brown%' OR item LIKE '%tater%' OR item LIKE '%lasagna%') AND date >= ?", (today,))

string = '<head>Tater Tot, Hashbrown, and Lasagna Tracker For This Week</head><body>'
for row in data:
    i = 0
    for col in row:
        if i == 0:
            if col not in string:
                string += '<br><b>' + col + '</b><br>'
        elif i == 1:
            string += '--' + col + '--<br>'
        elif i == 2:
            string += col + ': '
        else:
            string += col + '<br>'
        i += 1
    # string += '</br>'
string += f'</body><br>With Love,<br>UCSC Menu App<br><br>Please do not hesitate to respond with any questions or concerns.<br>Data as of {today}.'

# me == my email address
# you == recipient's email address
me = me_email
you = you_email


# Create message container - the correct MIME type is multipart/alternative.
msg = MIMEMultipart('alternative')
msg['Subject'] = "Tater Tot, Hashbrown, and Lasagna Tracker - Week of " + str(datetime.date.today())
msg['From'] = me
msg['To'] = you

# Create the body of the message (a plain-text and an HTML version).
html = string

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(string, 'plain')
part2 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.
msg.attach(part1)
msg.attach(part2)


mail = smtplib.SMTP('smtp.gmail.com', 587)

mail.ehlo()

mail.starttls()

mail.login(str(me), login_pass)
mail.sendmail(me, you, msg.as_string())
mail.quit()