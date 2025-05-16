from Model import database
from Model.clients import Clients
from Model.room import Room
from Model.reservation import Reservation

def add_client_to_database(client: Clients, database: database.ListClients):
    try:
        database.add_client(client)
        print(f"Client {client} added to the database.")
    except Exception as e:
        print(f"Error adding client to database: {e}")

def add_room_to_database(room: Room, database: database.ListRoom):
    try:
        database.add_room(room)
        print(f"Room {room} added to the database.")
    except Exception as e:
        print(f"Error adding room to database: {e}")

def affiche_reservable_room(database: database.ListRoom):
    try:
        for room in database.list_room:
            if room.is_available():
                print(f"Room {room} is available.")
            else:
                print(f"Room {room} is not available.")
    except Exception as e:
        print(f"Error checking room availability: {e}")

def client_see_reservation(client: Clients):
    try:
        #affichage des reservations du client
        for reservation in database.ListReservation.list_reservation:
            if reservation.client == client:
                print(f"Reservation {reservation} for client {client}.")
            else:
                print(f"No reservations found for client {client}.")
    except Exception as e:
        print(f"Error checking client reservations: {e}")
    
def identify_if_room_available_during_period(database: database.ListRoom, start_date, end_date):
    try:
        for room in database.list_room:
            if room.is_available(start_date, end_date):
                print(f"Room {room} is available from {start_date} to {end_date}.")
            else:
                print(f"Room {room} is not available from {start_date} to {end_date}.")
    except Exception as e:
        print(f"Error checking room availability during period: {e}")

def affiche_available_room_on_period(database: database.ListRoom, start_date, end_date):
    try:
        for room in database.list_room:
            if room.is_available(start_date, end_date):
                print(f"Room {room} is available from {start_date} to {end_date}.")
            else:
                print(f"Room {room} is not available from {start_date} to {end_date}.")
    except Exception as e:
        print(f"Error checking room availability on period: {e}")

def client_make_reservation_on_period(client: Clients, start_date, end_date):
    try:
        #affichage des salles dispopnibles durant la periode 
        affiche_available_room_on_period(database.ListRoom, start_date, end_date)
        #creation de la reservation pour la salle que le client choisi
        room = input("Enter the room you want to reserve: ")
        reservation = Reservation(client, room, start_date, end_date)   
        #ajout de la reservation dans la base de donnee
        database.ListReservation.add_reservation(reservation)
        print(f"Reservation {reservation} made for client {client} from {start_date} to {end_date}.")
    except Exception as e:
        print(f"Error making reservation: {e}")

def client_cancel_reservation(client: Clients, reservation: Reservation):
    try:
        #annulation de la reservation
        database.ListReservation.remove_reservation(reservation)
        print(f"Reservation {reservation} cancelled for client {client}.")
    except Exception as e:
        print(f"Error cancelling reservation: {e}") 


        