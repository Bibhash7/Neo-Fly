import os
from django_ratelimit.decorators import ratelimit
from flightApp.models import Flights, Passengers
from datetime import datetime
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from utils.validate_email import validate_emai_pattern
import utils.email_notification as notification
from concurrent.futures import ThreadPoolExecutor
from here_debugger.debug import here_debug
import utils.create_pdf as ticket
import logging
from utils.constants import (
    FlightAttributes,
    PassengerAttributes,
    NoAttribute,
    ErrorMessage,
    SuccessMessage,
    BookingEmail,
    CanecllationEmail,
    Attachment
)
logging.basicConfig(
    filename= os.environ.get("LOGFILE"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filemode='a'
)
pool = ThreadPoolExecutor(max_workers=2)

@api_view(['POST'])
def add_flight(request):
    try:
        flight_number = request.data.get(FlightAttributes.FLIGHT_NUMBER.value, NoAttribute.EMPTY_STRING.value)
        operating_airLines = request.data.get(FlightAttributes.OPERATING_AIRLINES.value, NoAttribute.EMPTY_STRING.value)
        departure_city = request.data.get(FlightAttributes.DEPARTURE_CITY.value, NoAttribute.EMPTY_STRING.value)
        arrival_city = request.data.get(FlightAttributes.ARRIVAL_CITY.value, NoAttribute.EMPTY_STRING.value)
        date_of_departure = request.data.get(FlightAttributes.DATE_OF_DEPARTURE.value, NoAttribute.EMPTY_STRING.value)
        time_of_departure = request.data.get(FlightAttributes.TIME_OF_DEPARTURE.value, NoAttribute.EMPTY_STRING.value)
        available_seats = request.data.get(FlightAttributes.AVAILABLE_SEATS.value, NoAttribute.EMPTY_STRING.value)
        
        if flight_number and operating_airLines and departure_city and arrival_city and date_of_departure and time_of_departure and available_seats:
            Flights(
                flight_number=int(flight_number),
                operating_airLines=operating_airLines,
                departure_city=departure_city,
                arrival_city= arrival_city,
                date_of_departure=datetime.strptime(date_of_departure, '%m-%d-%Y').date(),
                time_of_departure=datetime.strptime(time_of_departure, '%m/%d/%y %H:%M:%S'),
                available_seats=int(available_seats)
                ).save()
            return Response({SuccessMessage.SUCCESS.value: SuccessMessage.DATA_STORED.value},status=status.HTTP_201_CREATED)
            
        else:
            logging.debug(ErrorMessage.MANDETORY_FIELD_MISSING.value)
            return Response({ErrorMessage.ERROR.value: ErrorMessage.MANDETORY_FIELD_MISSING.value}, status=status.HTTP_400_BAD_REQUEST)
            
    
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def fetch_filghts(request):
    try:
        flights = Flights.nodes.all()
        list_of_filghts = [flight.serialize() for flight in flights]
        
        #TODO: Pagientation
        return Response({SuccessMessage.SUCCESS.value: list_of_filghts}, status=status.HTTP_200_OK)
    
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def update_fight(request, pk):
    try:
        flight = Flights.nodes.get(flight_number=pk)
        
        departure_city = request.data.get(FlightAttributes.DEPARTURE_CITY.value, NoAttribute.EMPTY_STRING.value)
        arrival_city = request.data.get(FlightAttributes.ARRIVAL_CITY.value, NoAttribute.EMPTY_STRING.value)
        date_of_departure = request.data.get(FlightAttributes.DATE_OF_DEPARTURE.value, NoAttribute.EMPTY_STRING.value)
        time_of_departure = request.data.get(FlightAttributes.TIME_OF_DEPARTURE.value, NoAttribute.EMPTY_STRING.value)
        
        if departure_city:
            flight.departure_city = departure_city
        elif arrival_city:
            flight.arrival_city = arrival_city
        elif date_of_departure:
            flight.date_of_departure = date_of_departure
        elif time_of_departure:
            flight.time_of_departure = time_of_departure
        else:
            return Response({ErrorMessage.ERROR.value: ErrorMessage.NOT_A_UPDATE_FIELD.value}, status=status.HTTP_400_BAD_REQUEST)
        flight.save()
        
        return Response({SuccessMessage.SUCCESS.value: SuccessMessage.DATA_UPDATED.value},status=status.HTTP_202_ACCEPTED)
    
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_filght(request,pk):
    try:
        flight = Flights.nodes.get(flight_number=pk)
        flight.delete()
        return Response({SuccessMessage.SUCCESS.value: SuccessMessage.DATA_REMOVED.value},status=status.HTTP_204_NO_CONTENT)
    
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def add_passenger(request):
    try:
        pid = request.data.get(PassengerAttributes.PID.value, NoAttribute.EMPTY_STRING.value)
        first_name = request.data.get(PassengerAttributes.FIRST_NAME.value, NoAttribute.EMPTY_STRING.value)
        last_name = request.data.get(PassengerAttributes.LAST_NAME.value, NoAttribute.EMPTY_STRING.value)
        age = request.data.get(PassengerAttributes.AGE.value, NoAttribute.EMPTY_STRING.value)
        email = request.data.get(PassengerAttributes.EMAIL.value, NoAttribute.EMPTY_STRING.value)
        phone_number = request.data.get(PassengerAttributes.PHONE_NUMBER.value, NoAttribute.EMPTY_STRING.value)
        
        if pid and first_name and last_name and age and email and phone_number:
            if validate_emai_pattern(email) == False:
                return Response({ErrorMessage.ERROR.value: ErrorMessage.EMAIL_PATTERN_ERROR.value}, status=status.HTTP_400_BAD_REQUEST)
            Passengers(
                pid = int(pid),
                first_name = first_name,
                last_name = last_name,
                age = int(age),
                email = email,
                phone_number = phone_number,
            ).save()
            return Response({SuccessMessage.SUCCESS.value: SuccessMessage.DATA_STORED.value},status=status.HTTP_201_CREATED)
        else:
            return Response({ErrorMessage.ERROR.value: ErrorMessage.MANDETORY_FIELD_MISSING.value}, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def fetch_passengers(request):
    try:
        passengers = Passengers.nodes.all()
        list_of_passengers = [passenger.serialize() for passenger in passengers]
        
        #TODO: Pagientation
        return Response({SuccessMessage.SUCCESS.value: list_of_passengers}, status=status.HTTP_200_OK)
    
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['PUT'])
def update_passenger(request, pk):
    try:
        passenger = Passengers.nodes.get(pid=pk)
        
        first_name = request.data.get(PassengerAttributes.FIRST_NAME.value, NoAttribute.EMPTY_STRING.value)
        last_name = request.data.get(PassengerAttributes.LAST_NAME.value, NoAttribute.EMPTY_STRING.value)
        email = request.data.get(PassengerAttributes.EMAIL.value, NoAttribute.EMPTY_STRING.value)
        phone_number = request.data.get(PassengerAttributes.PHONE_NUMBER.value, NoAttribute.EMPTY_STRING.value)
        
        if first_name:
            passenger.first_name = first_name
        elif last_name:
            passenger.last_name = last_name
        elif email:
            passenger.email = email
        elif phone_number:
            passenger.phone_number = phone_number
        else:
            return Response({ErrorMessage.ERROR.value: ErrorMessage.NOT_A_UPDATE_FIELD.value}, status=status.HTTP_400_BAD_REQUEST)
        
        passenger.save()
        return Response({SuccessMessage.SUCCESS.value: SuccessMessage.DATA_UPDATED.value},status=status.HTTP_202_ACCEPTED)
    
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def delete_passenger(request,pk):
    try:
        passenger = Passengers.nodes.get(pid=pk)
        passenger.delete()
        return Response({SuccessMessage.SUCCESS.value: SuccessMessage.DATA_REMOVED.value},status=status.HTTP_204_NO_CONTENT)
    
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
@ratelimit(key='ip', rate='5/m', block=False)
@api_view(['GET'])
def search_flights(request):
    try:
        is_rate_limited = getattr(request, 'limited', False)
        if is_rate_limited:
            return Response({ErrorMessage.ERROR.value: ErrorMessage.SEARCH_RATE_LIMIT_EXCEEDED.value}, status=status.HTTP_403_FORBIDDEN)
        
        departure_city = request.data.get(FlightAttributes.DEPARTURE_CITY.value, NoAttribute.EMPTY_STRING.value)
        arrival_city = request.data.get(FlightAttributes.ARRIVAL_CITY.value, NoAttribute.EMPTY_STRING.value)
        date_of_departure = request.data.get(FlightAttributes.DATE_OF_DEPARTURE.value, NoAttribute.EMPTY_STRING.value)
        flights = Flights.nodes.filter(departure_city=departure_city, arrival_city=arrival_city,date_of_departure=datetime.strptime(date_of_departure, '%Y-%m-%d').date())
        
        if flights:
            list_of_filghts = [flight.serialize() for flight in flights]
            return Response({SuccessMessage.SUCCESS.value: list_of_filghts}, status=status.HTTP_200_OK)
        
        else:
            return Response({ErrorMessage.ERROR.value: ErrorMessage.FLIGHT_NOT_FOUND.value}, status=status.HTTP_404_NOT_FOUND)
        
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    
    
@ratelimit(key='ip', rate='5/d', block=False)    
@api_view(['POST'])
def book_flight(request):
    try:
        is_rate_limited = getattr(request, 'limited', False)
        if is_rate_limited:
            return Response({ErrorMessage.ERROR.value: ErrorMessage.BOOKING_RATE_LIMIT_EXCEEDED.value}, status=status.HTTP_403_FORBIDDEN)
        
        pid = request.data.get(PassengerAttributes.PID.value, NoAttribute.EMPTY_STRING.value)
        flight_number = request.data.get(FlightAttributes.FLIGHT_NUMBER.value, NoAttribute.EMPTY_STRING.value)
        
        if pid and flight_number:
            passenger = Passengers.nodes.get(pid=pid)
            flight = Flights.nodes.get(flight_number=flight_number)
        
            if flight.available_seats == 0:
                logging.debug(ErrorMessage.REGRET.value)
                return Response({ErrorMessage.ERROR.value: ErrorMessage.REGRET.value}, status=status.HTTP_400_BAD_REQUEST)
            
            if passenger.booking.is_connected(flight) == False:
                passenger.booking.connect(flight)
                flight.available_seats -=1
                flight.save()
                ticket.create_ticket(
                    passenger.first_name,
                    passenger.last_name,
                    flight.departure_city,
                    flight.arrival_city,
                    flight.time_of_departure,
                )
                
                pool.submit(
                    notification.send_email_notification, 
                    BookingEmail.SUBJECT.value.format(flight.departure_city,flight.arrival_city, flight.date_of_departure), 
                    BookingEmail.BODY.value.format(passenger.first_name,flight.departure_city,flight.arrival_city), 
                    [passenger.email],
                    Attachment.ATTACHMENT_FILE_PATH.value,
                ) 
                         
                return Response({SuccessMessage.SUCCESS.value: SuccessMessage.BOOKED.value},status=status.HTTP_200_OK)
            else:
                logging.debug(ErrorMessage.ALREADY_BOOKED.value)
                return Response({ErrorMessage.ERROR.value: ErrorMessage.ALREADY_BOOKED.value}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            logging.debug(ErrorMessage.MANDETORY_FIELD_MISSING.value)
            return Response({ErrorMessage.ERROR.value: ErrorMessage.MANDETORY_FIELD_MISSING.value}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def cancel_flight(request):
    try:
        pid = request.data.get(PassengerAttributes.PID.value, NoAttribute.EMPTY_STRING.value)
        flight_number = request.data.get(FlightAttributes.FLIGHT_NUMBER.value, NoAttribute.EMPTY_STRING.value)
        
        if pid and flight_number:
            passenger = Passengers.nodes.get(pid=pid)
            flight = Flights.nodes.get(flight_number=flight_number)
            if passenger.booking.is_connected(flight):
                passenger.booking.disconnect(flight)
                flight.available_seats +=1
                flight.save()
                pool.submit(
                    notification.send_email_notification, 
                    CanecllationEmail.SUBJECT.value.format(flight.departure_city,flight.arrival_city, flight.date_of_departure), 
                    CanecllationEmail.BODY.value.format(passenger.first_name,flight.departure_city,flight.arrival_city), 
                    [passenger.email],
                    None
                )        
                return Response({SuccessMessage.SUCCESS.value: SuccessMessage.CANCELLED.value},status=status.HTTP_200_OK)
            else:
                logging.debug(ErrorMessage.NO_BOOKING.value)
                return Response({ErrorMessage.ERROR.value: ErrorMessage.NO_BOOKING.value}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            logging.debug(ErrorMessage.MANDETORY_FIELD_MISSING.value)
            return Response({ErrorMessage.ERROR.value: ErrorMessage.MANDETORY_FIELD_MISSING.value}, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as error:
        logging.error(error)
        return Response({ErrorMessage.ERROR.value: ErrorMessage.INTERNAL_SERVAR_ERROR.value}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
