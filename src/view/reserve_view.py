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

        self.selected_client = None
        self.start_datetime = None
        self.end_datetime = None
        self.selected_room = ("Aucune", "Aucun type")  # Valeur temporaire

        self.step_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.step_frame.pack(fill="both", expand=True)

        self.show_choose_client_frame()

    # === ÉTAPE 1 ===
    def show_choose_client_frame(self):
        self.clear_step_frame()
        self.step_client_frame = ctk.CTkFrame(self.step_frame)
        self.step_client_frame.pack(pady=20, padx=20, fill="both", expand=True)

        date_frame = ctk.CTkFrame(self.step_client_frame, fg_color="transparent")
        date_frame.pack(pady=10)

        self.debut_entry = DateEntry(
            date_frame, date_pattern="dd/mm/yyyy", locale="fr_FR"
        )
        self.debut_entry.pack(side="left", padx=5)
        self.start_time = ctk.CTkEntry(date_frame, placeholder_text="HH:MM")
        self.start_time.pack(side="left", padx=5)

        self.fin_entry = DateEntry(
            date_frame, date_pattern="dd/mm/yyyy", locale="fr_FR"
        )
        self.fin_entry.pack(side="left", padx=5)
        self.end_time = ctk.CTkEntry(date_frame, placeholder_text="HH:MM")
        self.end_time.pack(side="left", padx=5)

        client_frame = ctk.CTkFrame(self.step_client_frame, fg_color="transparent")
        client_frame.pack(pady=10)
        self.client_var = ctk.StringVar()
        self.client_combobox = ctk.CTkComboBox(
            client_frame, variable=self.client_var, state="readonly", width=300
        )
        self.client_combobox.pack()
        self.load_clients()

        ctk.CTkButton(
            self.step_client_frame, text="Suivant", command=self.choose_client_next
        ).pack(pady=20)

    def choose_client_next(self):
        self.selected_client = self.client_combobox.get()
        self.start_datetime = self.parse_datetime(
            self.debut_entry, self.start_time.get()
        )
        self.end_datetime = self.parse_datetime(self.fin_entry, self.end_time.get())

        if not self.selected_client or not self.start_datetime or not self.end_datetime:
            self.show_error("Veuillez remplir tous les champs.")
            return
        if (self.end_datetime - self.start_datetime) < timedelta(minutes=30):
            self.show_error("Durée minimale : 30 minutes.")
            return

        self.show_choose_room_frame()

    # === ÉTAPE 2 ===
    def show_choose_room_frame(self):
        self.clear_step_frame()
        self.step3_frame = ctk.CTkFrame(self.step_frame)
        self.step3_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            self.step3_frame,
            text="Récapitulatif de la réservation",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=10)

        ctk.CTkLabel(self.step3_frame, text=f"Client : {self.selected_client}").pack()
        ctk.CTkLabel(self.step3_frame, text=f"Début : {self.start_datetime}").pack()
        ctk.CTkLabel(self.step3_frame, text=f"Fin : {self.end_datetime}").pack()

        # Salle temporaire
        ctk.CTkLabel(
            self.step3_frame,
            text=f"Salle : {self.selected_room[0]} - {self.selected_room[1]}",
        ).pack()

        ctk.CTkButton(
            self.step3_frame, text="Confirmer", command=self.confirm_reservation
        ).pack(pady=20)

        ctk.CTkButton(
            self.step3_frame,
            text="Annuler",
            fg_color="red",
            command=self.controller.show_accueil,
        ).pack()

    # === CONFIRMATION ===
    def confirm_reservation(self):
        client_id = self.selected_client.split("(")[-1].strip(")")
        salle_id = self.selected_room[0]

        success = self.db.reserver_salle(
            client_id, salle_id, self.start_datetime, self.end_datetime
        )
        if success:
            self.controller.show_confirmation()
        else:
            self.show_error("La salle n'est plus disponible.")

    # === UTILITAIRES ===
    def clear_step_frame(self):
        for widget in self.step_frame.winfo_children():
            widget.destroy()

    def load_clients(self):
        clients = self.db.list_clients.list_client
        client_list = [f"{c.FirstName} {c.LastName} ({c.identity})" for c in clients]
        self.client_combobox.configure(values=client_list)

    def parse_datetime(self, date_entry, time_str):
        try:
            time_obj = datetime.strptime(time_str, "%H:%M").time()
            return datetime.combine(date_entry.get_date(), time_obj)
        except Exception:
            return None

    def show_error(self, message):
        err = ctk.CTkToplevel(self)
        err.title("Erreur")
        ctk.CTkLabel(err, text=message).pack(padx=20, pady=10)
        ctk.CTkButton(err, text="OK", command=err.destroy).pack(pady=5)
