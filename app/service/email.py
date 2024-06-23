import smtplib
import os

def send_email(book, updated_book, percent):
    email_rementente = os.getenv("EMAIL_REMETENTE")
    email_destinatario = os.getenv("EMAIL_DESTINATARIO")
    password_generated = os.getenv("PASSWORD_GENERATED")

    message = f"Subject: Price of {book['name']} has changed!\n\nThe price has changed from {book['price']} to {updated_book.price}! The percent is {percent}%. Here is the link: {book['url']}"
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(email_rementente,password_generated)
    server.sendmail(
    email_rementente,
    email_destinatario,
    message.encode('utf-8'))
    server.quit()
