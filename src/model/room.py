class ErrorRoom(Exception):
    pass


class Room:
    def __init__(self, Name: str, type: str, capacity: int):
        self.nom = Name
        self.type = type  # Corrigé : affecter le paramètre type, pas le type str
        self.capacity = capacity  # Corrigé : affecter le paramètre capacity, pas int

        # Correction logique des capacités maximales (la description dit capacité max, donc condition < ou >)
        if type == "Informatique":
            if capacity > 4 or capacity < 1:
                raise ErrorRoom("Informatique room capacity must be between 1 and 4.")
        elif type == "Conférence":
            if capacity > 10 or capacity < 4:
                raise ErrorRoom("Conférence room capacity must be between 4 and 10.")
        elif type == "Standard":
            if capacity > 4 or capacity < 1:
                raise ErrorRoom("Standard room capacity must be between 1 and 4.")
        else:
            raise ErrorRoom("Invalid room type.")

    def to_dict(self):
        return {"nom": self.nom, "type": self.type, "capacity": self.capacity}

    def __str__(self):
        return f"Room {self.nom} ({self.type}), capacity: {self.capacity}"
