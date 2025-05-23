import unittest
from datetime import datetime, timedelta
from clients import Clients, ErrorClients
from room import Room, ErrorRoom
from reservation import Reservation, ErrorReservation


class TestClients(unittest.TestCase):
    def test_client_creation(self):
        client = Clients("Doe", "John", "john@example.com", "secret")
        self.assertEqual(client.LastName, "Doe")
        self.assertEqual(client.FirstName, "John")
        self.assertEqual(client.mail, "john@example.com")
        self.assertTrue(client.identity)  # uuid generated

    def test_client_to_from_dict(self):
        client = Clients("Doe", "Jane", "jane@example.com", "pwd")
        d = client.to_dict()
        self.assertEqual(d["nom"], "Doe")
        self.assertEqual(d["prenom"], "Jane")
        self.assertEqual(d["mail"], "jane@example.com")
        self.assertEqual(d["password"], "pwd")
        client2 = Clients.from_dict(d)
        self.assertEqual(client2.LastName, "Doe")
        self.assertEqual(client2.FirstName, "Jane")

    def test_client_identity_unique(self):
        c1 = Clients("A", "B", "a@b.com")
        c2 = Clients("A", "B", "a@b.com")
        self.assertNotEqual(c1.identity, c2.identity)


class TestRoom(unittest.TestCase):
    def test_room_valid(self):
        r1 = Room("Room 1", "Informatique", 4)
        r2 = Room("Room 2", "Conférence", 10)
        r3 = Room("Room 3", "Standard", 3)
        self.assertEqual(r1.nom, "Room 1")
        self.assertEqual(r2.type, "Conférence")
        self.assertEqual(r3.capacity, 3)

    def test_room_invalid_type(self):
        with self.assertRaises(ErrorRoom):
            Room("BadRoom", "Invalid", 3)

    def test_room_invalid_capacity(self):
        with self.assertRaises(ErrorRoom):
            Room("RoomTooBig", "Informatique", 5)
        with self.assertRaises(ErrorRoom):
            Room("RoomTooBig", "Conférence", 15)
        with self.assertRaises(ErrorRoom):
            Room("RoomTooBig", "Standard", 6)

    def test_room_to_dict(self):
        r = Room("RoomDict", "Standard", 2)
        d = r.to_dict()
        self.assertEqual(d, {"nom": "RoomDict", "type": "Standard", "capacity": 2})


class TestReservation(unittest.TestCase):
    def setUp(self):
        self.client = Clients("Smith", "Will", "will@example.com", "pass123")
        self.room = Room("Conf Room", "Conférence", 8)
        self.start = datetime.now()
        self.end = self.start + timedelta(hours=2)

    def test_reservation_creation(self):
        res = Reservation(self.client, self.room, self.start, self.end)
        self.assertEqual(res.client, self.client)
        self.assertEqual(res.room, self.room)
        self.assertEqual(res.debut, self.start)
        self.assertEqual(res.fin, self.end)
        self.assertTrue(res.id)

    def test_reservation_to_from_dict(self):
        res = Reservation(self.client, self.room, self.start, self.end)
        d = res.to_dict()
        self.assertEqual(d["client_id"], self.client.identity)
        self.assertEqual(d["room_id"], self.room.nom)
        self.assertEqual(d["debut"], self.start.isoformat())
        self.assertEqual(d["fin"], self.end.isoformat())

        # from_dict needs clients_list and rooms_list for lookup
        clients_list = [self.client]
        rooms_list = [self.room]
        res2 = Reservation.from_dict(d, clients_list, rooms_list)
        self.assertEqual(res2.client.identity, self.client.identity)
        self.assertEqual(res2.room.nom, self.room.nom)
        self.assertEqual(res2.debut, self.start)
        self.assertEqual(res2.fin, self.end)

    def test_reservation_str(self):
        res = Reservation(self.client, self.room, self.start, self.end)
        s = str(res)
        self.assertIn(self.client.LastName, s)
        self.assertIn(self.room.nom, s)
        self.assertIn(str(res.id), s)


if __name__ == "__main__":
    unittest.main()
