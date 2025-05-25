from src.Model.clients import Clients
from src.Model.room import Room
import uuid
from datetime import datetime


class Reservation:
    def __init__(
        self,
        client: Clients,
        room: Room,
        debut: datetime,
        fin: datetime,
        id: str = str(uuid.uuid4()),
    ):
        self.client = client
        self.room = room
        self.debut = debut
        self.fin = fin
        self.id = id if id else str(uuid.uuid4())

    def to_dict(self):
        return {
            "id": self.id,
            "client_id": self.client.identity,
            "room_id": self.room.nom,
            "debut": self.debut.isoformat(),
            "fin": self.fin.isoformat(),
            "id": self.id,
        }

    @classmethod
    def from_dict(cls, data, clients_list, rooms_list):
        client = next(c for c in clients_list if c.identity == data["client_id"])
        room = next(r for r in rooms_list if r.nom == data["room_id"])
        debut = datetime.fromisoformat(data["debut"])
        fin = datetime.fromisoformat(data["fin"])

        reservation = cls(client, room, debut, fin)
        reservation.id = data.get("id")  # Restaurer l’id de la réservation
        return reservation


class ErrorReservation(Exception):
    pass
