import random

list_id=[]
class Error_room(Exception):
    pass
class Error_clients(Exception):
    pass
class room:
    def __init__(self, Name:str):
        self.nom = Name
        self.type = str
        self.capacity = 0
    def __str__(self):
        return f"Room {self.nom} with capacity of {self.capacite} personnes."
    def add_room(self, type:str, capacity:int):
        self.type = type
        self.capacity = capacity
        return self.type, self.capacity

class clients:
    def __init__(self, LastName:str, FirstName:str, mail:str):
        self.LastName = LastName
        self.FirstName = FirstName
        self.mail = mail
        self.identity = self.identity()
        def __str__(self):
            return f"Client {self.LastName} {self.FirstName} with mail {self.mail} and is number is {self.identity}."
        def identity(self):
            self.identity=random.randint(1,9999)
            if self.identity in list_id:
                identity(self)
            else:
                list_id.append(self.identity)
                return self.identity
        def add_client(self, LastName:str, FirstName:str, mail:str):
            self.LastName = LastName
            self.FirstName = FirstName
            self.mail = mail
            self.identity = self.identity()
            if self.identity in list_id:
                identity(self)
            else:
                list_id.append(self.identity)
                return self.identity
        def remove_client(self, LastName: str, FirstName: str,client: [clients]):
            for i in client:
                if i.LastName == LastName and i.FirstName == FirstName:
                    client.remove(i)
                    list_id.remove(i)
                    return client
                else:
                    raise Error_clients("Client not found")
            
    





