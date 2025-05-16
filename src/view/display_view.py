import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import os


class DisplayView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="transparent")

        # Configuration de la grille principale
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Notebook pour les différents modes d'affichage
        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Création des onglets
        self.create_clients_tab()
        self.create_rooms_tab()
        self.create_reservations_tab()
        self.create_availability_tab()

    def create_clients_tab(self):
        """Onglet d'affichage des clients"""
        tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(tab, text="Clients")

        # Treeview
        columns = ("ID", "Nom", "Prénom", "Email")
        self.clients_tree = ttk.Treeview(
            tab, columns=columns, show="headings", selectmode="browse"
        )

        for col in columns:
            self.clients_tree.heading(col, text=col)
            self.clients_tree.column(col, width=150)

        # Scrollbar
        vsb = ttk.Scrollbar(tab, orient="vertical", command=self.clients_tree.yview)
        self.clients_tree.configure(yscrollcommand=vsb.set)

        # Placement
        self.clients_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        # Bouton de rafraîchissement
        refresh_btn = ctk.CTkButton(
            tab, text="🔄 Actualiser", command=self.load_clients, width=100
        )
        refresh_btn.grid(row=1, column=0, pady=5)

        self.load_clients()

    def create_rooms_tab(self):
        """Onglet d'affichage des salles"""
        tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(tab, text="Salles")

        columns = ("ID", "Type", "Capacité")
        self.rooms_tree = ttk.Treeview(tab, columns=columns, show="headings")

        for col in columns:
            self.rooms_tree.heading(col, text=col)
            self.rooms_tree.column(col, width=120)

        vsb = ttk.Scrollbar(tab, orient="vertical", command=self.rooms_tree.yview)
        self.rooms_tree.configure(yscrollcommand=vsb.set)

        self.rooms_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        refresh_btn = ctk.CTkButton(tab, text="🔄 Actualiser", command=self.load_rooms)
        refresh_btn.grid(row=1, column=0, pady=5)

        self.load_rooms()

    def create_reservations_tab(self):
        """Onglet d'affichage des réservations par client"""
        tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(tab, text="Réservations")

        # Contrôles de recherche
        control_frame = ctk.CTkFrame(tab, fg_color="transparent")
        control_frame.grid(row=0, column=0, pady=10, sticky="ew")

        ctk.CTkLabel(control_frame, text="Rechercher client :").pack(
            side="left", padx=5
        )

        self.client_search = ctk.CTkComboBox(control_frame, state="readonly", width=300)
        self.client_search.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(
            control_frame, text="🔍 Rechercher", command=self.load_reservations
        )
        search_btn.pack(side="left", padx=5)

        # Tableau des réservations
        columns = ("Salle", "Type", "Début", "Fin", "Durée")
        self.reservations_tree = ttk.Treeview(tab, columns=columns, show="headings")

        for col in columns:
            self.reservations_tree.heading(col, text=col)
            self.reservations_tree.column(col, width=150)

        vsb = ttk.Scrollbar(
            tab, orient="vertical", command=self.reservations_tree.yview
        )
        self.reservations_tree.configure(yscrollcommand=vsb.set)

        self.reservations_tree.grid(row=1, column=0, sticky="nsew")
        vsb.grid(row=1, column=1, sticky="ns")

        self.load_clients_list()

    def create_availability_tab(self):
        """Onglet de recherche de disponibilités"""
        tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(tab, text="Disponibilités")

        # Contrôles de date
        date_frame = ctk.CTkFrame(tab, fg_color="transparent")
        date_frame.grid(row=0, column=0, pady=10, sticky="ew")

        ctk.CTkLabel(date_frame, text="Début :").pack(side="left", padx=5)
        self.start_date = DateEntry(
            date_frame, date_pattern="dd/mm/yyyy", locale="fr_FR"
        )
        self.start_date.pack(side="left", padx=5)

        ctk.CTkLabel(date_frame, text="Fin :").pack(side="left", padx=5)
        self.end_date = DateEntry(date_frame, date_pattern="dd/mm/yyyy", locale="fr_FR")
        self.end_date.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(
            date_frame, text="🔍 Rechercher", command=self.check_availability
        )
        search_btn.pack(side="left", padx=10)

        # Tableau des résultats
        columns = ("ID Salle", "Type", "Capacité")
        self.availability_tree = ttk.Treeview(tab, columns=columns, show="headings")

        for col in columns:
            self.availability_tree.heading(col, text=col)
            self.availability_tree.column(col, width=150)

        vsb = ttk.Scrollbar(
            tab, orient="vertical", command=self.availability_tree.yview
        )
        self.availability_tree.configure(yscrollcommand=vsb.set)

        self.availability_tree.grid(row=1, column=0, sticky="nsew")
        vsb.grid(row=1, column=1, sticky="ns")

    # Méthodes de chargement des données
    def load_clients(self):
        """Charge la liste des clients"""
        self.clients_tree.delete(*self.clients_tree.get_children())
        for client in self.db.lister_clients():
            self.clients_tree.insert(
                "",
                "end",
                values=(client["id"], client["nom"], client["prenom"], client["email"]),
            )

    def load_rooms(self):
        """Charge la liste des salles"""
        self.rooms_tree.delete(*self.rooms_tree.get_children())
        for salle in self.db.lister_salles():
            self.rooms_tree.insert(
                "", "end", values=(salle["id"], salle["type"], salle["capacite"])
            )

    def load_clients_list(self):
        """Met à jour la liste déroulante des clients"""
        clients = [
            f"{c['prenom']} {c['nom']} ({c['id']})" for c in self.db.lister_clients()
        ]
        self.client_search.configure(values=clients)

    def load_reservations(self):
        """Charge les réservations du client sélectionné"""
        client_info = self.client_search.get()
        if not client_info:
            return

        client_id = client_info.split("(")[-1].strip(")")
        reservations = self.db.lister_reservations_client(client_id)

        self.reservations_tree.delete(*self.reservations_tree.get_children())

        for res in reservations:
            salle = self.db.obtenir_salle_par_id(res["salle_id"])
            debut = datetime.fromisoformat(res["debut"])
            fin = datetime.fromisoformat(res["fin"])
            duree = fin - debut

            self.reservations_tree.insert(
                "",
                "end",
                values=(
                    salle["id"],
                    salle["type"],
                    debut.strftime("%d/%m/%Y %H:%M"),
                    fin.strftime("%d/%m/%Y %H:%M"),
                    str(duree),
                ),
            )

    def check_availability(self):
        """Vérifie les disponibilités"""
        debut = datetime.combine(self.start_date.get_date(), datetime.min.time())
        fin = datetime.combine(self.end_date.get_date(), datetime.min.time())

        salles = self.db.lister_salles_disponibles(debut, fin)

        self.availability_tree.delete(*self.availability_tree.get_children())
        for salle in salles:
            self.availability_tree.insert(
                "", "end", values=(salle["id"], salle["type"], salle["capacite"])
            )

    def update_all(self):
        """Rafraîchit toutes les données"""
        self.load_clients()
        self.load_rooms()
        self.load_clients_list()
