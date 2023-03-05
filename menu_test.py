import smtplib
import ssl
from email.message import EmailMessage

email_sender = 'ucscmenuapp@gmail.com'
email_password = 'zhubiwjiwzhktqct'
email_receiver = 'titan36541@gmail.com'

subject = 'Hello World'
body = """This email was sent using Python :)"""

em = EmailMessage()
em['From'] = email_sender
em['To'] = email_receiver
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    smtp.login(email_sender, email_password)
    smtp.sendmail(email_sender, email_receiver, em.as_string())