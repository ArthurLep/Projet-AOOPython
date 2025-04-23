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
        return f"Room {self.nom} with capacity of {self.capacity} person."
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

class list_client(clients):
    def __init__(self, clients:clients):
        self.clients = clients
        self.list_client = []
    def add_client(self, client:clients):
        if len(self.list_client) < 10:
            self.list_client.append(client)
        else:
            raise Error_clients("The list is full.")
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
        self.list_room = [""]
        reservable = [""]
        full = [""]
    def add_room(self, room:room):
            self.reservable.append(room)
    def __str__(self):
        return f"List of rooms: {self.list_room}."
    def reservable(self, room:room):

        for room in self.list_room:
            if room.capacity > 0:
                self.reservable.append(room)
        return self.reservable
    def reserve(self, room:room, client:clients):
        if room in self.list_room and client in self.list_client:
            room.capacity -= 1
            if room.capacity == 0:
                self.full.append(room)
                self.reservable.remove(room)
            return self.full
        else:
            raise Error_room("Room or client not found.")




