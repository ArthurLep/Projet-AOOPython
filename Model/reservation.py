import uuid
from datetime import date
from Model.clients import Clients
from Model.room import Room

class ErrorReservation(Exception):
    pass

class Reservation:
    def __init__(self, client: Clients, room: Room, start_date: date, end_date: date):
        self.client = client
        self.room = room
        self.start_date = start_date
        self.end_date = end_date
        self.id = str(uuid.uuid4())
    def __str__(self):
        return f"Reservation {self.id} for {self.client} in {self.room} from {self.start_date} to {self.end_date}."
