import customtkinter as ctk
from tkinter import ttk

from src.Model.reservation import Reservation


class DisplayReservation(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.client_search = None
        self.room_search = None
        self.reservations_tree = None
        self.room_reservations_tree = None
        self.create_reservations_tab()

    def create_reservations_tab(self):
        """Onglet : réservations par client"""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(tab, text="Réservations")

        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

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

    def load_clients_list(self):
        """Remplit la liste déroulante des clients"""
        clients = [
            f"{c.FirstName} {c.LastName} ({c.identity})"
            for c in self.db.list_clients.list_client
        ]
        self.client_search.configure(values=clients)

    def load_reservations(self):
        """Affiche les réservations d’un client donné"""
        client_info = self.client_search.get()
        if not client_info:
            return

        client_id = client_info.split("(")[-1].strip(")")

        all_reservations = self.db.list_reservations.list_reservation
        reservations = [
            res for res in all_reservations if res.client.identity == client_id
        ]

        self.reservations_tree.delete(*self.reservations_tree.get_children())

        for res in reservations:
            salle = self.db.obtenir_salle_par_id(
                res.room.nom
            )  # Assure-toi que c’est bien 'nom'
            debut = res.debut
            fin = res.fin
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
