import smtplib
from email.mime.text import MIMEText

EMAIL = "yourgmail@gmail.com"
APP_PASSWORD = "YOUR_16_CHARACTER_APP_PASSWORD"

def send_email(to_email, subject, body):
    msg = MIMEText(body)

    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = to_email

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, APP_PASSWORD)
    server.send_message(msg)
    server.quit()