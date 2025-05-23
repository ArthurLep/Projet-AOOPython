import json
import os
from .clients import Clients, ErrorClients
from .room import Room, ErrorRoom
from .reservation import Reservation

class ListClients:
    def __init__(self):
        self.clients = []
        self.load_from_json()

    def add_client(self, client: Clients):
        if client not in self.clients:
            self.clients.append(client)
            self.save_to_json()
        else:
            raise ErrorClients("Client already exists in the list.")

    def save_to_json(self):
        data = [c.to_dict() for c in self.clients]
        with open("users.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self):
        if os.path.exists("users.json"):
            with open("users.json", "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.clients = [Clients.from_dict(d) for d in data]
                except json.JSONDecodeError:
                    self.clients = []

    def remove_client(self, client: Clients):
        if client in self.clients:
            self.clients.remove(client)
            self.save_to_json()
        else:
            raise ErrorClients("Client not found in the list.")

class ListRoom:
    def __init__(self):
        self.rooms = []
        self.load_from_json()

    def add_room(self, room: Room):
        if room not in self.rooms:
            self.rooms.append(room)
            self.save_to_json()
        else:
            raise ErrorRoom("Room already exists in the list.")

    def save_to_json(self):
        data = [r.to_dict() for r in self.rooms]
        with open("rooms.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self):
        if os.path.exists("rooms.json"):
            with open("rooms.json", "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.rooms = [Room.from_dict(d) for d in data]
                except json.JSONDecodeError:
                    self.rooms = []

    def remove_room(self, room: Room):
        if room in self.rooms:
            self.rooms.remove(room)
            self.save_to_json()
        else:
            raise ErrorRoom("Room not found in the list.")

class ListReservation:
    def __init__(self, clients_list: ListClients, rooms_list: ListRoom):
        self.reservations = []
        self.clients_list = clients_list
        self.rooms_list = rooms_list
        self.load_from_json()

    def add_reservation(self, reservation: Reservation):
        if reservation not in self.reservations:
            self.reservations.append(reservation)
            self.save_to_json()
        else:
            raise Exception("Reservation already exists in the list.")

    def save_to_json(self):
        data = [r.to_dict() for r in self.reservations]
        with open("reservations.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self):
        if os.path.exists("reservations.json"):
            with open("reservations.json", "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                    self.reservations = [Reservation.from_dict(d, self.clients_list.clients, self.rooms_list.rooms) for d in data]
                except json.JSONDecodeError:
                    self.reservations = []

    def remove_reservation(self, reservation: Reservation):
        if reservation in self.reservations:
            self.reservations.remove(reservation)
            self.save_to_json()
        else:
            raise Exception("Reservation not found.")

class Database:
    def __init__(self):
        self.list_clients = ListClients()
        self.list_rooms = ListRoom()
        self.list_reservations = ListReservation(self.list_clients, self.list_rooms)

    def list_available_rooms(self, debut, fin, type_salle=None):
        salles = self.list_rooms.rooms
        if type_salle and type_salle != "Tous":
            salles = [s for s in salles if s.type_room == type_salle]
        available = []
        for salle in salles:
            # Vérifier qu'aucune réservation ne chevauche la période
            if all(not (res.room.nom == salle.nom and not (fin <= res.debut or debut >= res.fin))
                   for res in self.list_reservations.reservations):
                available.append(salle)
        return available

    def reserver_salle(self, client_id, salle_nom, debut, fin):
        client = next((c for c in self.list_clients.clients if c.identity == client_id), None)
        room = next((r for r in self.list_rooms.rooms if r.nom == salle_nom), None)
        if not client:
            raise ValueError(f"Client with id {client_id} not found.")
        if not room:
            raise ValueError(f"Room with name {salle_nom} not found.")

        # Vérifier disponibilité
        for res in self.list_reservations.reservations:
            if res.room.nom == salle_nom and not (fin <= res.debut or debut >= res.fin):
                raise ValueError("Room not available during the requested period.")

        reservation = Reservation(client, room, debut, fin)
        self.list_reservations.add_reservation(reservation)
        return reservation
