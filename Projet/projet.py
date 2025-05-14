import random
import uuid
from datetime import date

class ErrorRoom(Exception):
    pass
class ErrorClients(Exception):
    pass
class admin:
    def __init__(self, LastName:str, FirstName:str, mail:str, password:str):##creation de la classe administrateur
        self.password = password
        self.LastName = LastName
        self.FirstName = FirstName
        self.mail = mail
    def __str__(self):
        return f"Admin {self.LastName} {self.FirstName} with mail {self.mail}."
class room:

    def __init__(self, Name:str,type:str, capacity:int):
        self.nom = Name
        self.type = str
        self.capacity = int
        self.type = type
        if type == "Informatique":
            if capacity > 4:
                raise ErrorRoom("The room is too small.")
        elif type == "Conférence":
            if capacity > 10:
                raise ErrorRoom("The room is too small.")
        elif type == "Standard":
            if capacity > 4:
                raise ErrorRoom("The room is too small.")
        else:
            raise ErrorRoom("Invalid room type.")     
class clients:
    def __init__(self, LastName:str, FirstName:str, mail:str, password:str):
        self.password = password
        self.LastName = LastName
        self.FirstName = FirstName
        self.mail = mail
        self.identity = str(uuid.uuid4())
        
    def __str__(self):
        return f"Client {self.LastName} {self.FirstName} with mail {self.mail} and is number is {self.identity}."
class list_client:
    def __init__(self, clients:clients):
        self.clients = clients
        self.list_client = []
    def add_client(self, client:clients):
        if client not in self.list_client:
            self.list_client.append(client)
        else:
            raise Error_clients("Client already exists in the list.")
    def __str__(self):
        return f"List of clients: {self.list_client}."
    def remove_client(self, client:clients):
        if client in self.list_client:
            self.list_client.remove(client)
        else:
            raise Error_clients("Client not found in the list.")
class list_room:
    def __init__(self, room:room):
        self.room = room
        self.list_room = []
    def add_room(self, room:room):
        if room not in self.list_room:
            self.list_room.append(room)
        else:
            raise ErrorRoom("Room already exists in the list.")
    def __str__(self):
        return f"List of rooms: {self.list_room}."
    def remove_room(self, room:room):
        if room in self.list_room:
            self.list_room.remove(room)
        else:
            raise ErrorRoom("Room not found in the list.")
class reservation:
    def __init__(self, client:clients, room:room, date_reservation:date):
        self.client = client
        self.room = room
        self.date_reservation = date_reservation
        self.id = str(uuid.uuid4())
    def __str__(self):
        return f"Reservation {self.id} for {self.client} in {self.room} on {self.date_reservation}."
class list_reservation:
    def __init__(self, reservation:reservation):
        self.reservation = reservation
        self.list_reservation = []
    def add_reservation(self, reservation:reservation):
        if reservation not in self.list_reservation:
            self.list_reservation.append(reservation)
        else:
            raise ErrorRoom("Reservation already exists in the list.")
    def __str__(self):
        return f"List of reservations: {self.list_reservation}."
    def remove_reservation(self, reservation:reservation):
        if reservation in self.list_reservation:
            self.list_reservation.remove(reservation)
        else:
            raise ErrorRoom("Reservation not found in the list.")