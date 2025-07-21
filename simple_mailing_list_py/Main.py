import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class GmailSender:
    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self.smtp.login(self.user, self.password)

    def send(self, recipient_email, subject='Mail', body='Contenuto mail'):
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.user
        msg['To'] = recipient_email

        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)

        html = open('template.html', 'r').read()
        html = html.replace('{{content}}', body)
        html_part = MIMEText(html, 'html')
        msg.attach(html_part)

        self.smtp.sendmail(self.user, recipient_email, msg.as_string())
        print("Sent email to " + recipient_email)

    def quit(self):
        self.smtp.quit()


EMAIL_USER = os.environ.get('EMAIL_USER')
EMAIL_PASS = os.environ.get('EMAIL_PASS')

gmail = GmailSender(EMAIL_USER, EMAIL_PASS)

with open('list.txt', 'r') as f:
    email_list = [line.strip() for line in f.readlines()]

for email in email_list:
    gmail.send(email, subject='Test', body='Contenuto di prova')

gmail.quit()
