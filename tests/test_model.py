import unittest
import os
import json
from datetime import datetime, timedelta
from model.clients import Clients, ErrorClients
from model.room import Room, ErrorRoom
from model.reservation import Reservation, ErrorReservation
from model.database import ListClients, ListRoom, ListReservation
import fonction  # ton fichier fonction.py avec les fonctions métier


class TestClients(unittest.TestCase):
    def test_create_client(self):
        c = Clients("Dupont", "Jean", "jean@example.com", "pwd123")
        self.assertEqual(c.LastName, "Dupont")
        self.assertEqual(c.FirstName, "Jean")
        self.assertTrue(c.identity)
        d = c.to_dict()
        self.assertIn("identity", d)
        c2 = Clients.from_dict(d)
        self.assertEqual(c2.LastName, "Dupont")


class TestRoom(unittest.TestCase):
    def test_room_valid_and_invalid(self):
        r = Room("Salle 1", "Informatique", 4)
        self.assertEqual(r.nom, "Salle 1")
        self.assertEqual(r.type, "Informatique")

        with self.assertRaises(ErrorRoom):
            Room("Salle Bad", "Invalide", 4)
        with self.assertRaises(ErrorRoom):
            Room("Salle Trop Grande", "Informatique", 10)


class TestReservation(unittest.TestCase):
    def setUp(self):
        self.client = Clients("Martin", "Alice", "alice@example.com")
        self.room = Room("Conf 1", "Conférence", 8)
        self.start = datetime.now()
        self.end = self.start + timedelta(hours=2)

    def test_reservation_create_and_dict(self):
        r = Reservation(self.client, self.room, self.start, self.end)
        d = r.to_dict()
        self.assertEqual(d["client_id"], self.client.identity)
        self.assertEqual(d["room_id"], self.room.nom)
        r2 = Reservation.from_dict(d, [self.client], [self.room])
        self.assertEqual(r2.client.identity, self.client.identity)
        self.assertEqual(r2.room.nom, self.room.nom)


class TestListClients(unittest.TestCase):
    def setUp(self):
        # Nettoyer fichier users.json avant chaque test
        if os.path.exists("users.json"):
            os.remove("users.json")
        self.db = ListClients()

    def test_add_and_remove_client(self):
        c = Clients("Test", "User", "test@example.com")
        self.db.add_client(c)
        self.assertIn(c, self.db.list_client)

        # Sauvegarde JSON test
        self.db.save_to_json()
        with open("users.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertTrue(any(item["identity"] == c.identity for item in data))

        self.db.remove_client(c)
        self.assertNotIn(c, self.db.list_client)
        with self.assertRaises(ErrorClients):
            self.db.remove_client(c)  # déjà supprimé


class TestListRoom(unittest.TestCase):
    def setUp(self):
        if os.path.exists("rooms.json"):
            os.remove("rooms.json")
        self.db = ListRoom()

    def test_add_and_remove_room(self):
        r = Room("SalleTest", "Standard", 3)
        self.db.add_room(r)
        self.assertIn(r, self.db.list_room)

        self.db.save_to_json()
        with open("rooms.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            self.assertTrue(any(item["nom"] == r.nom for item in data))

        self.db.remove_room(r)
        self.assertNotIn(r, self.db.list_room)
        with self.assertRaises(ErrorRoom):
            self.db.remove_room(r)  # déjà supprimée


class TestListReservation(unittest.TestCase):
    def setUp(self):
        self.db = ListReservation()
        self.client = Clients("Res", "User", "res@example.com")
        self.room = Room("SalleRes", "Standard", 2)
        self.start = datetime.now()
        self.end = self.start + timedelta(hours=1)
        self.reservation = Reservation(self.client, self.room, self.start, self.end)

    def test_add_reservation(self):
        self.db.add_reservation(self.reservation)
        self.assertIn(self.reservation, self.db.list_reservation)

        with self.assertRaises(ErrorRoom):
            # ajouter 2x la même réservation doit échouer
            self.db.add_reservation(self.reservation)


class TestFonctions(unittest.TestCase):
    def setUp(self):
        # Création de bases pour fonctions
        self.clients_db = ListClients()
        self.rooms_db = ListRoom()
        self.reservations_db = ListReservation()

        self.client = Clients("Fonction", "Tester", "fonc@example.com")
        self.room = Room("SalleFonction", "Standard", 3)

        self.clients_db.add_client(self.client)
        self.rooms_db.add_room(self.room)

    def test_add_client_to_database(self):
        c = Clients("New", "Client", "newclient@example.com")
        fonction.add_client_to_database(c, self.clients_db)
        self.assertIn(c, self.clients_db.list_client)

    def test_add_room_to_database(self):
        r = Room("NouvelleSalle", "Standard", 4)
        fonction.add_room_to_database(r, self.rooms_db)
        self.assertIn(r, self.rooms_db.list_room)

    def test_affiche_reservable_room(self):
        # Note: is_available() doit être implémentée sur Room pour que ce test soit complet
        # On simule ici pour éviter erreur
        for room in self.rooms_db.list_room:
            room.is_available = lambda *args, **kwargs: True
        fonction.affiche_reservable_room(self.rooms_db)

    def test_client_make_and_cancel_reservation(self):
        start = datetime.now()
        end = start + timedelta(hours=1)

        # patch is_available pour autoriser
        self.room.is_available = lambda reservations, start_date, end_date: True

        fonction.client_make_reservation_on_period(self.client, self.room, start, end,
                                                   self.rooms_db, self.reservations_db)
        self.assertEqual(len(self.reservations_db.list_reservation), 1)

        res = self.reservations_db.list_reservation[0]
        fonction.client_cancel_reservation(self.client, res, self.reservations_db)
        self.assertEqual(len(self.reservations_db.list_reservation), 0)

    def test_supp_client_and_room(self):
        fonction.supp_client(self.client, self.clients_db)
        self.assertNotIn(self.client, self.clients_db.list_client)

        fonction.supp_room(self.room, self.rooms_db)
        self.assertNotIn(self.room, self.rooms_db.list_room)


if __name__ == "__main__":
    unittest.main()
