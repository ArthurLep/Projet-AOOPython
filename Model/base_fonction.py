from Model.clients import Clients
from Model.room import Room
from Model.reservation import Reservation
from Model.database import ListClients, ListRoom, ListReservation

def add_client_to_database(client: Clients, clients_db: ListClients):
    try:
        clients_db.add_client(client)
        print(f"Client {client} added.")
    except Exception as e:
        print(f"Error: {e}")

def add_room_to_database(room: Room, rooms_db: ListRoom):
    try:
        rooms_db.add_room(room)
        print(f"Room {room} added.")
    except Exception as e:
        print(f"Error: {e}")

def affiche_reservable_room(rooms_db: ListRoom, reservations: list, start_date, end_date):
    for room in rooms_db.list_room:
        if room.is_available(reservations, start_date, end_date):
            print(f"{room} is available.")
        else:
            print(f"{room} is NOT available.")

def client_see_reservation(client: Clients, reservations_db: ListReservation):
    found = False
    for reservation in reservations_db.list_reservation:
        if reservation.client.identity == client.identity:
            print(reservation)
            found = True
    if not found:
        print(f"No reservations found for {client}.")

def client_make_reservation_on_period(client: Clients, room: Room, start_date, end_date,
                                      rooms_db: ListRoom, reservations_db: ListReservation):
    if room.is_available(reservations_db.list_reservation, start_date, end_date):
        reservation = Reservation(client, room, start_date, end_date)
        reservations_db.add_reservation(reservation)
        print(f"Reservation confirmed: {reservation}")
    else:
        print(f"{room} is not available during that period.")

def client_cancel_reservation(client: Clients, reservation: Reservation, reservations_db: ListReservation):
    try:
        if reservation.client.identity == client.identity:
            reservations_db.remove_reservation(reservation)
            print(f"Reservation cancelled: {reservation}")
        else:
            print("This reservation doesn't belong to the client.")
    except Exception as e:
        print(f"Error: {e}")

def supp_client(client: Clients, clients_db: ListClients):
    try:
        clients_db.remove_client(client)
        print(f"Client {client} removed.")
    except Exception as e:
        print(f"Error: {e}")

def supp_room(room: Room, rooms_db: ListRoom):
    try:
        rooms_db.remove_room(room)
        print(f"Room {room} removed.")
    except Exception as e:
        print(f"Error: {e}")