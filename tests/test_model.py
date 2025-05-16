from Model import database
from Model import clients
from Model import room
from Model import reservation

def test_class_client():
    """Test the Clients class"""
    client = clients.Clients("John", "Doe", "mail", "123456789")
    assert client.first_name == "John"
    assert client.last_name == "Doe"
    assert client.email == "mail"


