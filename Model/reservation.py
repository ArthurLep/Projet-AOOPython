from Model.clients import Clients
from Model.room import Room
import uuid
from datetime import date

class Reservation:
    def __init__(self, client:clients, room:room, date_reservation:date):
        self.client = client
        self.room = room
        self.date_reservation = date_reservation
        self.id = str(uuid.uuid4())
    def __str__(self):
        return f"Reservation {self.id} for {self.client} in {self.room} on {self.date_reservation}."

class ErrorReservation(Exception):
    pass
