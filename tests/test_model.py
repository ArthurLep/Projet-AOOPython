from datetime import date, timedelta
from Model.clients import Clients, ErrorClients
from Model.room import Room, ErrorRoom
from Model.reservation import Reservation, ErrorReservation
from Model.storage import ListClients, ListRoom, ListReservation

def test_clients():
    print("=== Test Clients ===")
    clients_db = ListClients()
    client1 = Clients("Dupont", "Jean", "jean.dupont@mail.com", "pass123")
    client2 = Clients("Martin", "Alice", "alice.martin@mail.com", "pass456")
    
    # Ajout client
    clients_db.add_client(client1)
    clients_db.add_client(client2)
    print(clients_db)
    
    # Test ajout doublon
    try:
        clients_db.add_client(client1)
    except ErrorClients as e:
        print("Caught expected exception:", e)
    
    # Suppression client
    clients_db.remove_client(client1)
    print(clients_db)
    
    # Suppression client absent
    try:
        clients_db.remove_client(client1)
    except ErrorClients as e:
        print("Caught expected exception:", e)

def test_rooms():
    print("\n=== Test Rooms ===")
    rooms_db = ListRoom()
    room1 = Room("Salle 101", "Standard", 4)
    room2 = Room("Salle 102", "Conférence", 8)
    
    # Ajout salle
    rooms_db.add_room(room1)
    rooms_db.add_room(room2)
    print(rooms_db)
    
    # Test ajout doublon
    try:
        rooms_db.add_room(room1)
    except ErrorRoom as e:
        print("Caught expected exception:", e)
    
    # Suppression salle
    rooms_db.remove_room(room1)
    print(rooms_db)
    
    # Suppression salle absente
    try:
        rooms_db.remove_room(room1)
    except ErrorRoom as e:
        print("Caught expected exception:", e)

def test_reservations():
    print("\n=== Test Reservations ===")
    reservations_db = ListReservation()
    clients_db = ListClients()
    rooms_db = ListRoom()
    
    # Création clients et salles
    client = Clients("Dupont", "Jean", "jean.dupont@mail.com", "pass123")
    room = Room("Salle 101", "Standard", 4)
    clients_db.add_client(client)
    rooms_db.add_room(room)
    
    start_date = date.today()
    end_date = start_date + timedelta(days=1)
    
    # Création réservation
    reservation1 = Reservation(client, room, start_date, end_date)
    reservations_db.add_reservation(reservation1)
    print(reservations_db)
    
    # Test ajout doublon
    try:
        reservations_db.add_reservation(reservation1)
    except ErrorReservation as e:
        print("Caught expected exception:", e)
    
    # Suppression réservation
    reservations_db.remove_reservation(reservation1)
    print(reservations_db)
    
    # Suppression réservation absente
    try:
        reservations_db.remove_reservation(reservation1)
    except ErrorReservation as e:
        print("Caught expected exception:", e)

def test_room_availability():
    print("\n=== Test Room Availability ===")
    rooms_db = ListRoom()
    reservations_db = ListReservation()
    
    room1 = Room("Salle 101", "Standard", 4)
    room2 = Room("Salle 102", "Conférence", 8)
    rooms_db.add_room(room1)
    rooms_db.add_room(room2)
    
    client = Clients("Dupont", "Jean", "jean.dupont@mail.com", "pass123")
    
    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after = today + timedelta(days=2)
    
    # Réservation sur Salle 101 du jour à demain
    reservation = Reservation(client, room1, today, tomorrow)
    reservations_db.add_reservation(reservation)
    
    # Fonction de disponibilité simple
    def is_room_available(room, start_date, end_date, reservations):
        for res in reservations.list_reservation:
            if res.room == room:
                # Vérifier chevauchement
                if not (end_date <= res.start_date or start_date >= res.end_date):
                    return False
        return True
    
    # Test disponibilité
    print(f"Salle 101 dispo aujourd'hui->demain:", is_room_available(room1, today, tomorrow, reservations_db))
    print(f"Salle 101 dispo demain->après-demain:", is_room_available(room1, tomorrow, day_after, reservations_db))
    print(f"Salle 102 dispo aujourd'hui->demain:", is_room_available(room2, today, tomorrow, reservations_db))

if __name__ == "__main__":
    test_clients()
    test_rooms()
    test_reservations()
    test_room_availability()
