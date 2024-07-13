from django.core.mail import EmailMessage
import logging

def send_email_notification(subject,body,recipients,ticket_path):
    try:
        email = EmailMessage(subject,body,to = recipients)
        if ticket_path is not None:
            with open(ticket_path, 'rb') as f:
                email.attach('Neo_fly_ticket.pdf', f.read(), 'application/pdf')
        email.send()
    except Exception as error:
        logging.error(error)