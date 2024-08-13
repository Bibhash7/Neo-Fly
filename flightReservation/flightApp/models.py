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
    
    def serialize(self):
        return {
            'flight_number': self.flight_number,
            'operating_airLines': self.operating_airLines,
            'departure_city': self.departure_city,
            'arrival_city': self.arrival_city,
            'date_of_departure': str(self.date_of_departure),
            'time_of_departure': str(self.time_of_departure),
            'available_seats': self.available_seats,
        }


class Passengers(StructuredNode):
    pid = IntegerProperty(unique_index=True)
    first_name = StringProperty(required=True)
    last_name = StringProperty(required=True)
    age = IntegerProperty(required=True)
    email = StringProperty(required=True)
    phone_number = StringProperty(required=True)
    booking = RelationshipTo(Flights,'BOOKED_TO')
    
    def serialize(self):
        return {
            "pid": self.pid,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "email": self.email,
            "phone_number": self.phone_number,
        
        }

    
    
    
    
    

# Create your models here.
