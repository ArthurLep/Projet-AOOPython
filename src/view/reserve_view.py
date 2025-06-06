import customtkinter as ctk
from tkcalendar import DateEntry
from datetime import datetime, timedelta


class ReserveView(ctk.CTkFrame):
    def __init__(self, parent, controller, db):
        super().__init__(parent)
        self.controller = controller
        self.db = db
        self.configure(fg_color="transparent")

        self.title_label = ctk.CTkLabel(
            self,
            text="Reserver une salle :",
            font=("Helvetica", 30),
            text_color="white",
        )
        self.title_label.pack(pady=(50, 20))

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
        self.step_client_frame = ctk.CTkFrame(self.step_frame, fg_color="transparent")
        self.step_client_frame.pack(pady=20, padx=20, fill="both", expand=True)

        date_frame = ctk.CTkFrame(self.step_client_frame, fg_color="transparent")
        date_frame.pack(pady=10, fill="x")

        start_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        start_frame.pack(pady=5, fill="x")
        start_label = ctk.CTkLabel(
            start_frame, text="Début :", width=80, anchor="w", font=("Helvetica", 20)
        )
        start_label.pack(side="left", padx=50)
        self.start_entry = DateEntry(
            start_frame,
            date_pattern="dd/mm/yyyy",
            locale="fr_FR",
            width=20,
            font=("Helvetica", 15),
        )
        self.start_entry.pack(side="left", padx=5)
        self.start_time = ctk.CTkEntry(
            start_frame,
            placeholder_text="HH:MM",
            justify="center",
            font=("Helvetica", 12),
            width=500,
        )
        self.start_time.pack(side="left", padx=15)

        end_frame = ctk.CTkFrame(date_frame, fg_color="transparent")
        end_frame.pack(pady=5, fill="x")
        end_label = ctk.CTkLabel(
            end_frame, text="Fin :", width=80, anchor="w", font=("Helvetica", 20)
        )
        end_label.pack(side="left", padx=50)
        self.end_entry = DateEntry(
            end_frame,
            date_pattern="dd/mm/yyyy",
            locale="fr_FR",
            width=20,
            font=("Helvetica", 15),
        )
        self.end_entry.pack(side="left", padx=5)
        self.end_time = ctk.CTkEntry(
            end_frame,
            placeholder_text="HH:MM",
            justify="center",
            font=("Helvetica", 12),
            width=500,
        )
        self.end_time.pack(side="left", padx=15)

        client_frame = ctk.CTkFrame(self.step_client_frame, fg_color="transparent")
        client_frame.pack(pady=5, fill="x")
        client_label = ctk.CTkLabel(
            client_frame, text="Client :", width=80, anchor="w", font=("Helvetica", 20)
        )
        client_label.pack(side="left", padx=50)
        self.client_var = ctk.StringVar()
        self.client_combobox = ctk.CTkComboBox(
            client_frame, variable=self.client_var, state="readonly", width=500
        )
        self.client_combobox.pack()
        self.load_clients()

        self.validate_btn = ctk.CTkButton(
            self.step_client_frame,
            text="Valider",
            command=self.choose_client_next,
            width=200,
            height=50,
            fg_color="green",
            hover_color="lightgreen",
            corner_radius=8,
            font=("Helvetica", 18),
        )
        self.validate_btn.pack(side="left", padx=(300, 0), pady=10)

    def choose_client_next(self):
        self.selected_client = self.client_combobox.get()
        self.start_datetime = self.parse_datetime(
            self.start_entry, self.start_time.get()
        )
        self.end_datetime = self.parse_datetime(self.end_entry, self.end_time.get())

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
        self.step_room_frame = ctk.CTkFrame(self.step_frame, fg_color="transparent")
        self.step_room_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            self.step_room_frame,
            text="Choix de la salle",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=10)

        salles_dispo = self.db.list_available_rooms_on_period(
            self.start_datetime, self.end_datetime
        )

        if not salles_dispo:
            ctk.CTkLabel(
                self.step_room_frame, text="Aucune salle disponible à ces horaires."
            ).pack(pady=10)
            ctk.CTkButton(
                self.step_room_frame,
                text="Retour",
                command=self.show_choose_client_frame,
            ).pack(pady=10)
            return

        salle_frame = ctk.CTkFrame(self.step_room_frame, fg_color="transparent")
        salle_frame.pack(pady=10)

        ctk.CTkLabel(salle_frame, text="Sélectionnez une salle disponible :").pack(
            pady=5
        )

        self.room_var = ctk.StringVar()
        self.room_map = {f"{salle.nom} - {salle.type}": salle for salle in salles_dispo}

        self.room_combobox = ctk.CTkComboBox(
            salle_frame,
            variable=self.room_var,
            values=list(self.room_map.keys()),
            state="readonly",
            width=400,
        )
        self.room_combobox.pack(pady=5)

        ctk.CTkButton(
            self.step_room_frame,
            text="Suivant",
            command=self.validate_room_choice,
        ).pack(pady=20)

    # === CONFIRMATION ===
    def confirm_reservation(self):
        client_id = self.selected_client.split("(")[-1].strip(")")
        salle_id = self.selected_room.id

        if not self.db.is_room_available(
            salle_id, self.start_datetime, self.end_datetime
        ):
            self.show_error("Cette salle est déjà réservée à ce créneau")
            return

        success = self.db.reserver_salle(
            client_id, salle_id, self.start_datetime, self.end_datetime
        )
        if success:
            self.controller.show_confirmation()
            self.reset()
        else:
            self.show_error("La salle n'est plus disponible.")

    # === UTILITAIRES ===
    def clear_step_frame(self):
        for widget in self.step_frame.winfo_children():
            widget.destroy()

    def load_clients(self):
        clients = self.db.list_clients.clients
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

    def validate_room_choice(self):
        selected = self.room_combobox.get()
        if not selected:
            self.show_error("Veuillez sélectionner une salle.")
            return

        self.selected_room = self.room_map[selected]  # Stocke l'objet Room
        self.show_summary_frame()

    def show_summary_frame(self):
        self.clear_step_frame()
        self.step_summary_frame = ctk.CTkFrame(self.step_frame, fg_color="transparent")
        self.step_summary_frame.pack(padx=20, pady=20, fill="both", expand=True)

        ctk.CTkLabel(
            self.step_summary_frame,
            text="Récapitulatif de la réservation",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=10)

        ctk.CTkLabel(
            self.step_summary_frame, text=f"Client : {self.selected_client}"
        ).pack(pady=5)
        ctk.CTkLabel(
            self.step_summary_frame,
            text=f"Début : {self.start_datetime.strftime('%d/%m/%Y %H:%M')}",
        ).pack(pady=5)
        ctk.CTkLabel(
            self.step_summary_frame,
            text=f"Fin : {self.end_datetime.strftime('%d/%m/%Y %H:%M')}",
        ).pack(pady=5)
        ctk.CTkLabel(
            self.step_summary_frame,
            text=f"Salle : {self.selected_room.nom} - {self.selected_room.type}",
        ).pack(pady=5)

        ctk.CTkButton(
            self.step_summary_frame, text="Confirmer", command=self.confirm_reservation
        ).pack(pady=20)

        ctk.CTkButton(
            self.step_summary_frame,
            text="Annuler",
            fg_color="red",
            command=self.controller.show_accueil,
        ).pack()

    def reset(self):
        self.selected_client = None
        self.selected_room = ("Aucune", "Aucun type")
        self.start_datetime = None
        self.end_datetime = None
        self.show_choose_client_frame()
