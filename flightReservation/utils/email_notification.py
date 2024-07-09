from django.core.mail import EmailMessage
import logging

def send_email_notification(subject,body,recipients):
    try:
        email = EmailMessage(subject,body,to = recipients)
        email.send()
    except Exception as error:
        logging.error(error)