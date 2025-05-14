import uuid

class ErrorClients(Exception):
    pass

class Clients:
    def __init__(self, LastName:str, FirstName:str, mail:str, password:str):
        self.password = password
        self.LastName = LastName
        self.FirstName = FirstName
        self.mail = mail
        self.identity = str(uuid.uuid4())
        
    def __str__(self):
        return f"Client {self.LastName} {self.FirstName} with mail {self.mail} and is number is {self.identity}."