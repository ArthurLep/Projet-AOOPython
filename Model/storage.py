import json
from datetime import datetime

def date_to_str(d):
    """Convertit une date en chaîne ISO."""
    return d.isoformat()

def str_to_date(s):
    """Convertit une chaîne ISO en date."""
    return datetime.fromisoformat(s).date()

def save_data(clients_db, rooms_db, reservations_db, filename="data.json"):
    """Sauvegarde les données clients, rooms, reservations dans un fichier JSON."""
    data = {
        "clients": [
            {
                "id": c.identity,
                "LastName": c.LastName,
                "FirstName": c.FirstName,
                "mail": c.mail,
                "password": c.password
            } for c in clients_db.list_client
        ],
        "rooms": [
            {
                "name": r.nom,
                "type": r.type,
                "capacity": r.capacity
            } for r in rooms_db.list_room
        ],
        "reservations": [
            {
                "id": res.id,
                "client_id": res.client.identity,
                "room_name": res.room.nom,
                "start_date": date_to_str(res.start_date),
                "end_date": date_to_str(res.end_date)
            } for res in reservations_db.list_reservation
        ]
    }
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Données sauvegardées dans {filename}")

def load_data(clients_db, rooms_db, reservations_db, filename="data.json"):
    """Charge les données depuis un fichier JSON vers les objets clients_db, rooms_db, reservations_db."""
    try:
        with open(filename, "r") as f:
            data = json.load(f)

        # Vider les listes actuelles
        clients_db.list_client.clear()
        rooms_db.list_room.clear()
        reservations_db.list_reservation.clear()

        # Charger les clients
        for cdata in data.get("clients", []):
            client = clients_db.Clients(
                cdata["LastName"],
                cdata["FirstName"],
                cdata["mail"],
                cdata["password"]
            )
            client.identity = cdata["id"]
            clients_db.list_client.append(client)

        # Charger les rooms
        for rdata in data.get("rooms", []):
            room = rooms_db.Room(
                rdata["name"],
                rdata["type"],
                rdata["capacity"]
            )
            rooms_db.list_room.append(room)

        # Charger les reservations
        for resdata in data.get("reservations", []):
            # Trouver client par id
            client = next((c for c in clients_db.list_client if c.identity == resdata["client_id"]), None)
            # Trouver room par nom
            room = next((r for r in rooms_db.list_room if r.nom == resdata["room_name"]), None)

            if client and room:
                start_date = str_to_date(resdata["start_date"])
                end_date = str_to_date(resdata["end_date"])
                reservation = reservations_db.Reservation(client, room, start_date, end_date)
                reservation.id = resdata["id"]
                reservations_db.list_reservation.append(reservation)

        print(f"Données chargées depuis {filename}")

    except FileNotFoundError:
        print(f"Fichier {filename} introuvable, démarrage avec des données vides.")
    except Exception as e:
        print(f"Erreur lors du chargement des données: {e}")
