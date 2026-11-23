import logging
import smtplib
from email.message import EmailMessage
from src.config import get_smtp_settings


def send_email(recipient, subject, body):
    settings = get_smtp_settings()
    message = EmailMessage()
    message["From"] = settings["from_email"]
    message["To"] = recipient
    message["Subject"] = subject
    message.set_content(body)

    # STARTTLS encrypts the connection after connecting to the SMTP server.
    with smtplib.SMTP(settings["host"], settings["port"], timeout=30) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(settings["username"], settings["password"])
        server.send_message(message)

    logging.info("Email successfully submitted to SMTP server for %s", recipient)
