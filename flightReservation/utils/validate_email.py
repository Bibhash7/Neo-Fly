from email_validator import validate_email, EmailNotValidError
import logging
 
def validate_emai_pattern(email):
    try:
        v = validate_email(email)
        return True
    except EmailNotValidError as error:
        logging.error(error)
        return False
    
        