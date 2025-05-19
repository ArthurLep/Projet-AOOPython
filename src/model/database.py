from .clients import Clients, ErrorClients
from .room import Room, ErrorRoom
from .reservation import Reservation
import json
import os


class ListClients:
    def __init__(self, clients: Clients = None):
        self.clients = clients
        self.list_client = []
        self.load_from_json()

    def add_client(self, client: Clients):
        if client not in self.list_client:
            self.list_client.append(client)
            self.save_to_json()
        else:
            raise ErrorClients("Client already exists in the list.")

    def save_to_json(self):
        data = [client.to_dict() for client in self.list_client]
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self):
        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.list_client = [Clients.from_dict(d) for d in data]
                except json.JSONDecodeError:
                    self.list_client = []

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
        self.load_from_json()

    def add_room(self, room: Room):
        if room not in self.list_room:
            self.list_room.append(room)
            self.save_to_json()
        else:
            raise ErrorRoom("Room already exists in the list.")

    def save_to_json(self):
        data = [room.to_dict() for room in self.list_room]
        with open("rooms.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self):
        if os.path.exists("rooms.json"):
            with open("rooms.json", "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.list_room = [Room.from_dict(d) for d in data]
                except json.JSONDecodeError:
                    self.list_room = []

    def __str__(self):
        return f"List of rooms: {self.list_room}."

    def remove_room(self, room: Room):
        if room in self.list_room:
            self.list_room.remove(room)
        else:
            raise ErrorRoom("Room not found in the list.")


class ListReservation:
    def __init__(self, reservation: Reservation = None):
        self.reservation = reservation
        self.list_reservation = []

    def add_reservation(self, reservation: Reservation):
        if reservation not in self.list_reservation:
            self.list_reservation.append(reservation)
        else:
            raise ErrorRoom("Reservation already exists in the list.")

    def __str__(self):
        return f"List of reservations: {self.list_reservation}."


class Database:
    def __init__(self):
        self.list_clients = ListClients()
        self.list_rooms = ListRoom()
        self.list_reservations = ListReservation()

    def listes_salles_disponibles(self, debut, fin, type_salle=None):
        salles = self.list_rooms.list_room
        if type_salle and type_salle != "Tous":
            salles = [s for s in salles if s.type_room == type_salle]
        return salles

    def reserver_salle(self, client_id, salle_id, debut, fin):
        return True
