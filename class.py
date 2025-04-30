import random
import datetime

list_id=[]

class Error_room(Exception):
    pass
class Error_clients(Exception):
    pass
class admin:
    def __init__(self, LastName:str, FirstName:str, mail:str, password:str):##creation de la classe administrateur
        self.password = password
        self.LastName = LastName
        self.FirstName = FirstName
        self.mail = mail
    def __str__(self):
        return f"Admin {self.LastName} {self.FirstName} with mail {self.mail}."
class room:## creation de la classe salle

    def __init__(self, Name:str):
        self.nom = Name
        self.type = str
        self.capacity = 0
    def __str__(self):
        return f"Room {self.nom} with capacity of {self.capacity} person."
    def add_room(self, type:str, capacity:int): ## creation de la fonction qui permet d'ajouter une salle
        if type == "Informatique":
            self.capacity = 4
        elif type == "Conférence":
            self.capacity = 10
        elif type == "Standard":
            self.capacity = 4
        else:
            raise Error_room("Invalid room type.")
        
class clients: ## creation de la classe client
    def __init__(self, LastName:str, FirstName:str, mail:str, password:str):
        self.password = password
        self.LastName = LastName
        self.FirstName = FirstName
        self.mail = mail
        self.identity = self.identity()
    def __str__(self):
        return f"Client {self.LastName} {self.FirstName} with mail {self.mail} and is number is {self.identity}."
    def identity(self):
        id = random.randint(1000, 9999)
        while id in list_id:
            id = random.randint(1000, 9999)
        list_id.append(id)
        return id

class list_client(clients):
    def __init__(self, clients:clients):
        self.clients = clients
        self.list_client = []
    def add_client(self, client:clients):
        if client not in self.list_client:
            self.list_client.append(client)
        else:
            raise Error_clients("Client already exists in the list.")
    def __str__(self):
        return f"List of clients: {self.list_client}."
    def remove_client(self, client:clients):
        if client in self.list_client:
            self.list_client.remove(client)
        else:
            raise Error_clients("Client not found in the list.")

class list_room(room):
    def __init__(self, room:room):
        self.room = room
        self.date = datetime.date()
        self.list_room = [""]
        self.reservable = [""]
        self.full = [""]
    def add_room(self, room:room):
            self.reservable.append(room)
    def __str__(self):
        return f"List of rooms: {self.list_room}."
    def free(self, room:room):
        for room in self.list_room:
            if room.capacity > 0:
                self.reservable.append(room)
        return self.reservable
    def unfree(self, room:room, client:clients):
        if room in self.list_room and client in self.list_client:
            room.capacity -= 1
            if room.capacity == 0:
                self.full.append(room)
                self.reservable.remove(room)
            return self.full
        else:
            raise Error_room("Room or client not found.")





