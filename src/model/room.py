class ErrorRoom(Exception):
    pass

class Room:

    def __init__(self, Name:str,type:str, capacity:int):
        self.nom = Name
        self.type = str
        self.capacity = int
        self.type = type
        if type == "Informatique":
            if capacity > 4:
                raise ErrorRoom("The room is too small.")
        elif type == "Conférence":
            if capacity > 10:
                raise ErrorRoom("The room is too small.")
        elif type == "Standard":
            if capacity > 4:
                raise ErrorRoom("The room is too small.")
        else:
            raise ErrorRoom("Invalid room type.")     