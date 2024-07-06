from django.db import models
from neomodel import StructuredNode, StringProperty, DateProperty, RelationshipTo, DateTimeProperty, IntegerProperty

class Flights(StructuredNode):
    flight_number = IntegerProperty(unique_index=True)
    operating_airLines = StringProperty(required=True)
    departure_city = StringProperty(required=True)
    arrival_city = StringProperty(required=True)
    date_of_departure = DateProperty(required=True)
    time_of_departure = DateTimeProperty(required=True)
    available_seats = IntegerProperty(required=True)


class Passengers(StructuredNode):
    pid = IntegerProperty(unique_index=True)
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    age = IntegerProperty(required=True)
    email = StringProperty(required=True)
    phone_number = StringProperty(required=True)
    booking = RelationshipTo(Flights,'BOOKED_TO')
    

    
    
    
    
    

# Create your models here.
