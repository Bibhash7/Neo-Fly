from django.core.mail import EmailMessage
from utils.constants import Attachment
import logging

def send_email_notification(subject,body,recipients,ticket_path):
    try:
        email = EmailMessage(subject,body,to = recipients)
        if ticket_path is not None:
            with open(ticket_path, 'rb') as f:
                email.attach(Attachment.ATTACHMENT_FILE_NAME.value, f.read(), 'application/pdf')
        email.send()
    except Exception as error:
        logging.error(error)