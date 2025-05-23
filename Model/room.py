class ErrorRoom(Exception):
    pass

class Room:
    def __init__(self, name: str, type: str, capacity: int):
        self.name = name
        self.type = type
        self.capacity = capacity

        if type == "Informatique" and capacity < 1 or capacity > 4:
            raise ErrorRoom("Informatique rooms must have 1 to 4 seats.")
        elif type == "Conférence" and (capacity < 5 or capacity > 10):
            raise ErrorRoom("Conférence rooms must have 5 to 10 seats.")
        elif type == "Standard" and (capacity < 1 or capacity > 4):
            raise ErrorRoom("Standard rooms must have 1 to 4 seats.")
        elif type not in ["Informatique", "Conférence", "Standard"]:
            raise ErrorRoom("Invalid room type.")

    def __str__(self):
        return f"{self.name} ({self.type}, {self.capacity} places)"

    def is_available(self, reservations: list, start_date, end_date):
        for res in reservations:
            if res.room.name == self.name:
                if not (end_date <= res.start_date or start_date >= res.end_date):
                    return False
        return True