from Model import database
from Model.clients import Clients
from Model.room import Room
from Model.reservation import Reservation
from datetime import datetime

def add_client_to_database(client: Clients, clients_db: database.ListClients):
    try:
        clients_db.add_client(client)
        print(f"Client {client} added to the database.")
    except Exception as e:
        print(f"Error adding client to database: {e}")

def add_room_to_database(room: Room, rooms_db: database.ListRoom):
    try:
        rooms_db.add_room(room)
        print(f"Room {room} added to the database.")
    except Exception as e:
        print(f"Error adding room to database: {e}")

def affiche_reservable_room(rooms_db: database.ListRoom, reservations_db: database.ListReservation):
    try:
        for room in rooms_db.list_room:
            if room.is_available(reservations_db.list_reservation):
                print(f"Room {room} is available.")
            else:
                print(f"Room {room} is not available.")
    except Exception as e:
        print(f"Error checking room availability: {e}")

def client_see_reservation(client: Clients, reservations_db: database.ListReservation):
    try:
        found = False
        for reservation in reservations_db.list_reservation:
            if reservation.client.identity == client.identity:
                print(f"Reservation {reservation} for client {client}.")
                found = True
        if not found:
            print(f"No reservations found for client {client}.")
    except Exception as e:
        print(f"Error checking client reservations: {e}")

def identify_if_room_available_during_period(rooms_db: database.ListRoom, reservations_db: database.ListReservation, start_date: datetime, end_date: datetime):
    try:
        for room in rooms_db.list_room:
            if room.is_available(reservations_db.list_reservation, start_date, end_date):
                print(f"Room {room} is available from {start_date} to {end_date}.")
            else:
                print(f"Room {room} is not available from {start_date} to {end_date}.")
    except Exception as e:
        print(f"Error checking room availability during period: {e}")

def affiche_available_room_on_period(rooms_db: database.ListRoom, reservations_db: database.ListReservation, start_date: datetime, end_date: datetime):
    try:
        for room in rooms_db.list_room:
            if room.is_available(reservations_db.list_reservation, start_date, end_date):
                print(f"Room {room} is available from {start_date} to {end_date}.")
            else:
                print(f"Room {room} is not available from {start_date} to {end_date}.")
    except Exception as e:
        print(f"Error checking room availability on period: {e}")

def client_make_reservation_on_period(client: Clients, rooms_db: database.ListRoom, reservations_db: database.ListReservation, start_date: datetime, end_date: datetime):
    try:
        # Affiche les salles disponibles durant la période
        available_rooms = [room for room in rooms_db.list_room if room.is_available(reservations_db.list_reservation, start_date, end_date)]
        if not available_rooms:
            print("No rooms available for this period.")
            return
        
        print("Available rooms:")
        for room in available_rooms:
            print(f"- {room.nom}")
        
        room_name = input("Enter the room name you want to reserve: ")
        # Trouve la salle correspondante
        room_to_reserve = next((r for r in available_rooms if r.nom == room_name), None)
        if not room_to_reserve:
            print(f"Room '{room_name}' not found or not available.")
            return
        
        reservation = Reservation(client, room_to_reserve, start_date, end_date)
        reservations_db.add_reservation(reservation)
        print(f"Reservation {reservation} made for client {client} from {start_date} to {end_date}.")
    except Exception as e:
        print(f"Error making reservation: {e}")

def client_cancel_reservation(client: Clients, reservation: Reservation, reservations_db: database.ListReservation):
    try:
        if reservation.client.identity != client.identity:
            print("This reservation does not belong to the client.")
            return
        reservations_db.remove_reservation(reservation)
        print(f"Reservation {reservation} cancelled for client {client}.")
    except Exception as e:
        print(f"Error cancelling reservation: {e}") 

def supp_client(client: Clients, clients_db: database.ListClients):
    try:
        clients_db.remove_client(client)
        print(f"Client {client} removed from the database.")
    except Exception as e:
        print(f"Error removing client from database: {e}")

def supp_room(room: Room, rooms_db: database.ListRoom):
    try:
        rooms_db.remove_room(room)
        print(f"Room {room} removed from the database.")
    except Exception as e:
        print(f"Error removing room from database: {e}")