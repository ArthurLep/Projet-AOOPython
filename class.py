
class Error_room(Exception):
    pass
class Error_clients(Exception):
    pass
class room:
    def __init__(self, type:str, capacity:int):
        self.type = type
        self.capacity = capacity
    def __str__(self):
        return f"Salle {self.nom} avec une capacité de {self.capacite} personnes."

class clients:
    def __init__(self, LastName:str, FirstName:str, mail:str, identity:int):
        self.LastName = LastName
        self.FirstName = FirstName
        self.mail = mail
        def __str__(self):
            return f"Client {self.LastName} {self.FirstName} avec l'email {self.mail}."

            