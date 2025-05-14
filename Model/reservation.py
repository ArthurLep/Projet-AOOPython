from Model.clients import clients
from Model.room import room
import uuid
from datetime import date

class reservation:
    def __init__(self, client:clients, room:room, date_reservation:date):
        self.client = client
        self.room = room
        self.date_reservation = date_reservation
        self.id = str(uuid.uuid4())
    def __str__(self):
        return f"Reservation {self.id} for {self.client} in {self.room} on {self.date_reservation}."

