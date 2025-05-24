import uuid


class ErrorRoom(Exception):
    pass


class Room:
    def __init__(self, Name: str, type: str, capacity: int):
        self.nom = Name
        self.capacity = capacity
        self.type = type
        self.id = str(uuid.uuid4())
        if type == "Informatique":
            if capacity < 1 or capacity > 4:
                raise ErrorRoom("The room is too small.")
        elif type == "Conférence":
            if capacity < 4 or capacity > 10:
                raise ErrorRoom("The room is too small.")
        elif type == "Standard":
            if capacity < 1 or capacity > 4:
                raise ErrorRoom("The room is too small.")
        else:
            raise ErrorRoom("Invalid room type.")

    @classmethod
    def from_dict(cls, data: dict):
        room = cls(
            Name=data.get("nom"),
            type=data.get("type"),
            capacity=data.get("capacity"),
        )
        room.id = data.get("id")
        return room

    def to_dict(self):
        return {
            "nom": self.nom,
            "type": self.type,
            "capacity": self.capacity,
            "id": self.id,
        }
