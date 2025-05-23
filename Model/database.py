from Model.clients import Clients, ErrorClients
from Model.room import Room, ErrorRoom
from Model.reservation import Reservation, ErrorReservation

class ListClients:
    def __init__(self):
        self.list_client = []

    def add_client(self, client: Clients):
        if client not in self.list_client:
            self.list_client.append(client)
        else:
            raise ErrorClients("Client already exists in the list.")

    def remove_client(self, client: Clients):
        if client in self.list_client:
            self.list_client.remove(client)
        else:
            raise ErrorClients("Client not found in the list.")

    def __str__(self):
        return f"Clients: {[str(c) for c in self.list_client]}"

class ListRoom:
    def __init__(self):
        self.list_room = []

    def add_room(self, room: Room):
        if room not in self.list_room:
            self.list_room.append(room)
        else:
            raise ErrorRoom("Room already exists in the list.")

    def remove_room(self, room: Room):
        if room in self.list_room:
            self.list_room.remove(room)
        else:
            raise ErrorRoom("Room not found in the list.")

    def __str__(self):
        return f"Rooms: {[str(r) for r in self.list_room]}"

class ListReservation:
    def __init__(self):
        self.list_reservation = []

    def add_reservation(self, reservation: Reservation):
        if reservation not in self.list_reservation:
            self.list_reservation.append(reservation)
        else:
            raise ErrorReservation("Reservation already exists in the list.")

    def remove_reservation(self, reservation: Reservation):
        if reservation in self.list_reservation:
            self.list_reservation.remove(reservation)
        else:
            raise ErrorReservation("Reservation not found.")

    def __str__(self):
        return f"Reservations: {[str(r) for r in self.list_reservation]}"