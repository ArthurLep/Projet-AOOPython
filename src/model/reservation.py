from .clients import Clients
from .room import Room
import uuid
from datetime import datetime


class Reservation:
    def __init__(self, client: Clients, room: Room, debut: datetime, fin: datetime):
        self.client = client
        self.room = room
        self.debut = debut
        self.fin = fin
        self.id = str(uuid.uuid4())

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client.identity,
            "room_id": self.room.nom,
            "debut": self.debut.isoformat(),
            "fin": self.fin.isoformat(),
        }

    @classmethod
    def from_dict(cls, data, clients_list, rooms_list):
        client = next(c for c in clients_list if c.identity == data["client_id"])
        room = next(r for r in rooms_list if r.nom == data["room_id"])
        debut = datetime.fromisoformat(data["debut"])
        fin = datetime.fromisoformat(data["fin"])
        return cls(client, room, debut, fin)

    def __str__(self):
        # Correction : 'date_reservation' n'existe pas, remplacer par début et fin
        return (f"Reservation {self.id} for {self.client} "
                f"in {self.room} from {self.debut.strftime('%Y-%m-%d %H:%M')} "
                f"to {self.fin.strftime('%Y-%m-%d %H:%M')}.")


class ErrorReservation(Exception):
    pass
