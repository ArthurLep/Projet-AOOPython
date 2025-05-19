import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime, timedelta


class ReserveView(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.configure(fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.create_date_widgets()
        self.create_client_widgets()
        self.create_room_filter()
        self.create_room_table()
        self.create_buttons()

        self.load_clients()

    def create_date_widgets(self):
        frame_dates = ctk.CTkFrame(self)
        frame_dates.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_dates, text="Début :").grid(row=0, column=0, padx=5)
        self.debut_entry = DateEntry(
            frame_dates,
            date_pattern="dd/mm/yyyy",
            locale="fr_FR",
            font=ctk.CTkFont(size=12),
        )
        self.debut_entry.grid(row=0, column=1, padx=5)

        self.start_time = ctk.CTkEntry(frame_dates, placeholder_text="HH:MM")
        self.start_time.grid(row=0, column=2, padx=5)

        ctk.CTkLabel(frame_dates, text="Fin :").grid(row=0, column=3, padx=5)
        self.fin_entry = DateEntry(
            frame_dates,
            date_pattern="dd/mm/yyyy",
            locale="fr_FR",
            font=ctk.CTkFont(size=12),
        )
        self.fin_entry.grid(row=0, column=4, padx=5)

        self.end_time = ctk.CTkEntry(frame_dates, placeholder_text="HH:MM")
        self.end_time.grid(row=0, column=5, padx=5)

    def create_client_widgets(self):
        frame_client = ctk.CTkFrame(self)
        frame_client.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_client, text="Client :").grid(row=0, column=0, padx=5)
        self.client_var = ctk.StringVar()
        self.client_combobox = ctk.CTkComboBox(
            frame_client, variable=self.client_var, state="readonly"
        )
        self.client_combobox.grid(row=0, column=1, padx=5, sticky="ew")

    def create_room_filter(self):
        frame_filter = ctk.CTkFrame(self)
        frame_filter.grid(row=2, column=0, pady=10, padx=10, sticky="ew")

        ctk.CTkLabel(frame_filter, text="Type de salle :").grid(row=0, column=0, padx=5)
        self.type_var = ctk.StringVar(value="Tous")
        self.type_combobox = ctk.CTkComboBox(
            frame_filter,
            values=["Tous", "Standard", "Conférence", "Informatique"],
            variable=self.type_var,
            command=self.update_rooms,
        )
        self.type_combobox.grid(row=0, column=1, padx=5, sticky="ew")

    def create_room_table(self):
        self.tree = ttk.Treeview(
            self,
            columns=("identity", "type_room", "capacity"),
            show="headings",
            selectmode="browse",
        )
        self.tree.heading("identity", text="ID")
        self.tree.heading("type_room", text="Type")
        self.tree.heading("capacity", text="Capacité")
        self.tree.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")

    def create_buttons(self):
        frame_buttons = ctk.CTkFrame(self)
        frame_buttons.grid(row=4, column=0, pady=10, sticky="se")

        ctk.CTkButton(
            frame_buttons,
            text="Annuler",
            fg_color="#FF5555",
            command=self.controller.show_accueil,
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            frame_buttons,
            text="Valider",
            fg_color="#55FF55",
            command=self.validate_reservation,
        ).pack(side="right", padx=5)

    def load_clients(self):
        clients = self.db.list_clients.list_client
        client_list = [f"{c.FirstName} {c.LastName} ({c.identity})" for c in clients]
        self.client_combobox.configure(values=client_list)

    def parse_datetime(self, date_entry, time_str):
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            return datetime.combine(date_entry.get_date(), time_obj)
        except:
            return None

    def update_rooms(self, *args):
        debut = self.parse_datetime(self.debut_entry, self.start_time.get())
        fin = self.parse_datetime(self.fin_entry, self.end_time.get())
        if not debut or not fin:
            return
        if (fin - debut) < timedelta(minutes=30):
            self.show_error("Durée minimale : 30 minutes")
            return

        type_salle = self.type_var.get() if self.type_var.get() != "Tous" else None
        salles = self.db.lister_salles_disponibles(debut, fin, type_salle)

        self.tree.delete(*self.tree.get_children())
        for salle in salles:
            self.tree.insert(
                "", "end", values=(salle.identity, salle.type_room, salle.capacity)
            )

    def validate_reservation(self):
        client_info = self.client_combobox.get()
        if not client_info:
            self.show_error("Veuillez sélectionner un client")
            return

        selected_item = self.tree.selection()
        if not selected_item:
            self.show_error("Veuillez sélectionner une salle")
            return

        client_id = client_info.split("(")[-1].strip(")")
        salle_id = self.tree.item(selected_item)["values"][0]

        debut = self.parse_datetime(self.debut_entry, self.start_time.get())
        fin = self.parse_datetime(self.fin_entry, self.end_time.get())

        if not debut or not fin:
            self.show_error("Format de date/heure invalide")
            return

        # Demande de confirmation
        confirm = tk.messagebox.askyesno(
            "Confirmer la réservation",
            f"Confirmer la réservation de la salle {salle_id} pour le client {client_id} ?",
        )

        if not confirm:
            return

        if self.db.reserver_salle(client_id, salle_id, debut, fin):
            self.controller.show_confirmation()
            self.update_rooms()
        else:
            self.show_error("La salle n'est plus disponible")

    def show_error(self, message):
        error_window = ctk.CTkToplevel(self)
        error_window.title("Erreur")
        ctk.CTkLabel(error_window, text=message).pack(padx=20, pady=10)
        ctk.CTkButton(error_window, text="OK", command=error_window.destroy).pack(
            pady=5
        )
