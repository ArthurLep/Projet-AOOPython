from .clients import Clients, ErrorClients
from .room import Room, ErrorRoom
from .reservation import Reservation, ErrorReservation
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
    def __init__(self, clients_list, rooms_list, reservation: Reservation = None):
        self.reservation = reservation
        self.clients_list = clients_list
        self.rooms_list = rooms_list
        self.list_reservation = []
        self.load_from_json()

    def add_reservation(self, reservation: Reservation):
        if reservation not in self.list_reservation:
            self.list_reservation.append(reservation)
            self.save_to_json()
        else:
            raise ErrorRoom("Reservation already exists in the list.")

    def save_to_json(self):
        data = [res.to_dict() for res in self.list_reservation]
        with open("reservations.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def load_from_json(self):
        if os.path.exists("reservations.json"):
            with open("reservations.json", "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)  # data est une liste de dict
                    self.list_reservation = [
                        Reservation.from_dict(d, self.clients_list, self.rooms_list)
                        for d in data
                    ]
                except (json.JSONDecodeError, ErrorReservation) as e:
                    print(f"Erreur lors du chargement des réservations : {e}")
                    self.list_reservation = []
        else:
            self.list_reservation = []

    def __str__(self):
        return f"List of reservations: {self.list_reservation}."


class Database:
    def __init__(self):
        self.list_clients = ListClients()
        self.list_rooms = ListRoom()
        self.list_reservations = ListReservation(
            self.list_clients.list_client, self.list_rooms.list_room
        )

    def list_available_rooms(self, debut, fin, type_salle=None):
        salles = self.list_rooms.list_room
        if type_salle and type_salle != "Tous":
            salles = [s for s in salles if s.type == type_salle]
        return salles

    def reserver_salle(self, client_id, salle_id, debut, fin):
        client = next(
            (c for c in self.list_clients.list_client if c.identity == client_id), None
        )
        salle = next((r for r in self.list_rooms.list_room if r.id == salle_id), None)
        if not client or not salle:
            return False

        reservation = Reservation(client, salle, debut, fin)

        try:
            self.list_reservations.add_reservation(reservation)
        except Exception as e:
            print(f"Erreur lors de l'ajout de réservation : {e}")
            return False

        return True

    def obtenir_salle_par_id(self, room_id):
        for room in self.list_rooms.list_room:
            if room.nom == room_id:
                return {
                    "id": room.nom,
                    "type": room.type,
                }
        return None

    def is_room_available(self, room_id, start_datetime, end_datetime):
        for reservation in self.list_reservations.list_reservation:
            if reservation.room.id == room_id:
                if not (
                    end_datetime <= reservation.debut
                    or start_datetime >= reservation.fin
                ):
                    return False
        return True
