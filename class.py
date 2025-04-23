list_id=[]
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
    def __init__(self, LastName:str, FirstName:str, mail:str):
        self.LastName = LastName
        self.FirstName = FirstName
        self.mail = mail
        self.identity = self.identity()
        def __str__(self):
            return f"Client {self.LastName} {self.FirstName} avec l'email {self.mail} et son numéro est {self.identity}."
        def identity(self):
            self.identity=random.randint(1,9999)
            if self.identity in list_id:
                identity(self)
            else:
                list_id.append(self.identity)
                return self.identity



