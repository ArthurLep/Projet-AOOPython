import uuid


class ErrorClients(Exception):
    pass


class Clients:
    def __init__(
        self,
        LastName: str,
        FirstName: str,
        mail: str,
        password: str = "",
        identity: str = None,
    ):
        self.password = password
        self.LastName = LastName
        self.FirstName = FirstName
        self.mail = mail
        self.identity = identity if identity else str(uuid.uuid4())

    def to_dict(self):
        return {
            "nom": self.LastName,
            "prenom": self.FirstName,
            "mail": self.mail,
            "password": self.password,
            "identity": self.identity,
        }

    @classmethod
    def from_dict(cls, data):
        client = cls(
            LastName=data["nom"],
            FirstName=data["prenom"],
            mail=data["mail"],
            password=data["password"],
        )
        client.identity = data["identity"]
        return client

    def __str__(self):
        return f"Client {self.LastName} {self.FirstName} with mail {self.mail} and is number is {self.identity}."
