from .clients import Clients, ErrorClients
from .room import Room, ErrorRoom
from .reservation import Reservation
import uuid
from datetime import date


class ListClients:
    def __init__(self, clients: Clients = None):
        self.clients = clients
        self.list_client = []

    def add_client(self, client: Clients):
        if client not in self.list_client:
            self.list_client.append(client)
        else:
            raise ErrorClients("Client already exists in the list.")

    def __str__(self):
        return f"List of clients: {self.list_client}."

    def remove_client(self, client: Clients):
        if client in self.list_client:
            self.list_client.remove(client)
        else:
            raise ErrorClients("Client not found in the list.")


class ListRoom:
    def __init__(self, room: Room = None):
        self.room = room
        self.list_room = []

    def add_room(self, room: Room):
        if room not in self.list_room:
            self.list_room.append(room)
        else:
            raise ErrorRoom("Room already exists in the list.")

    def __str__(self):
        return f"List of rooms: {self.list_room}."

    def remove_room(self, room: Room):
        if room in self.list_room:
            self.list_room.remove(room)
        else:
            raise ErrorRoom("Room not found in the list.")


class ListReservation:
    def __init__(self, reservation: Reservation):
        self.reservation = reservation
        self.list_reservation = []

    def add_reservation(self, reservation: Reservation):
        if reservation not in self.list_reservation:
            self.list_reservation.append(reservation)
        else:
            raise ErrorRoom("Reservation already exists in the list.")

    def __str__(self):
        return f"List of reservations: {self.list_reservation}."
