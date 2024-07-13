from enum import Enum

class FlightAttributes(Enum):
    FLIGHT_NUMBER = "flight_number"
    OPERATING_AIRLINES = "operating_airLines"
    DEPARTURE_CITY = "departure_city"
    ARRIVAL_CITY = "arrival_city"
    DATE_OF_DEPARTURE = "date_of_departure"
    TIME_OF_DEPARTURE = "time_of_departure"
    AVAILABLE_SEATS = "available_seats"
    
class PassengerAttributes(Enum):
    PID = "pid"
    FIRST_NAME = "first_name"
    LAST_NAME = "last_name"
    AGE = "age"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    
class NoAttribute(Enum):
    EMPTY_STRING = ""
    
class ErrorMessage(Enum):
    ERROR = "Error"
    MANDETORY_FIELD_MISSING = "Please provide all fields."
    INTERNAL_SERVAR_ERROR = "Internal Server Error."
    NOT_A_UPDATE_FIELD = "Either the field is not present or the field is not updatable or values missing in the updatable field."
    ALREADY_BOOKED = "A booking for this flight already exists."
    NO_BOOKING = "No booking for this flight have been associated with this person."
    REGRET = "All seats are occupied, please opt for another flight."
    EMAIL_PATTERN_ERROR = "Please enter a valid email id."
    
class SuccessMessage(Enum):
    SUCCESS = "Success"
    DATA_STORED = "Data stored successfully."
    DATA_UPDATED = "Data updated successfully."
    DATA_REMOVED = "Data removed successfully."
    BOOKED = "Hola, Flight booked. Grab your seat."
    CANCELLED = "Booking has been cancelled successfully."
    
class BookingEmail(Enum):
    SUBJECT = "Booking Conformation | {} to {}, Date: {}"
    BODY = """
         Dear {},
         
         Your flight for {} to {} has been booked! 
         Desclaimer: Please reach 1 hour before for luggage checking and verification. 
        
         Thanks 
         Team NeoFly 
    """

class CanecllationEmail(Enum):
    SUBJECT = "Caneclled  | {} to {}, Date: {}"
    BODY = """
         Dear {}, 
         
         Your flight for {} to {} has been cancelled. 
        
         Thanks 
         Team NeoFly 
    """
    
class Attachment(Enum):
    ATTACHMENT_FILE_PATH = "C:\\Users\\bibha\\Desktop\ALL-Project-Oct-23\\DNF\\flightReservation\static\\Neo_fly_ticket.pdf"
    ATTACHMENT_FILE_NAME = "Neo_fly_ticket.pdf"
    
    
    
    