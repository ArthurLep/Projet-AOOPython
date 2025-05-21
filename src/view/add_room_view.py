import customtkinter as ctk
from tkinter import messagebox
from src.Model.room import Room, ErrorRoom


class AddRoomView(ctk.CTkFrame):
    """View to add a new room."""

    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.configure(fg_color="transparent")

        # Configuration de la grille
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        # Widgets
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the view"""

        self.title_label = ctk.CTkLabel(
            self,
            text="Ajouter une nouvelle salle :",
            font=("Helvetica", 30),
            text_color="white",
        )
        self.title_label.pack(pady=(50, 20))

        self.id_entry = ctk.CTkEntry(
            self,
            placeholder_text="Identifiant de la salle",
            justify="center",
            width=400,
            height=50,
            font=("Helvetica", 20),
        )
        self.id_entry.pack(padx=20, pady=20)

        capacity_frame = ctk.CTkFrame(self, fg_color="transparent")
        capacity_frame.pack(pady=20, padx=5)

        self.capacity_label = ctk.CTkLabel(
            capacity_frame, text="Capacité :", font=("Helvetica", 25)
        )
        self.capacity_label.pack(side="left", padx=(0, 10))

        self.capacity_entry = ctk.CTkEntry(
            capacity_frame,
            placeholder_text="1",
            justify="center",
            width=100,
            height=50,
            font=("Helvetica", 20),
        )
        self.capacity_entry.pack(side="left")

        type_frame = ctk.CTkFrame(self, fg_color="transparent")
        type_frame.pack(padx=20, pady=10)

        self.type_var = ctk.StringVar(value="Type de salle")
        self.type_menu = ctk.CTkComboBox(
            type_frame,
            variable=self.type_var,
            values=["Standard", "Conférence", "Informatique"],
            state="readonly",
            width=300,
            height=50,
            font=("Helvetica", 20),
        )
        self.type_menu.pack(side="left")

        # Boutons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=100)

        btn_frame.grid_columnconfigure(0, weight=1)
        btn_frame.grid_columnconfigure(1, weight=1)

        self.validate_btn = ctk.CTkButton(
            btn_frame,
            text="Valider",
            command=self._valider,
            width=100,
            height=80,
            fg_color="green",
            hover_color="lightgreen",
            corner_radius=8,
            font=("Helvetica", 18),
        )
        self.validate_btn.pack(side="right", padx=(100, 0), pady=10)

        self.erase_btn = ctk.CTkButton(
            btn_frame,
            text="Annuler",
            command=self._annuler,
            width=100,
            height=40,
            fg_color="red",
            hover_color="lightcoral",
            corner_radius=8,
            font=("Helvetica", 18),
        )
        self.erase_btn.pack(side="left", padx=(0, 0), pady=10)

    def _valider(self):
        """Validate the informations entered by the user"""
        room_id = self.id_entry.get().strip()
        room_type = self.type_var.get()
        capacity = self.capacity_entry.get().strip()

        if not all([room_id, room_type, capacity]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return

        try:
            capacity = int(capacity)
            if capacity <= 0:
                raise ValueError("La capacité doit être un nombre positif.")
        except ValueError as e:
            messagebox.showerror("Erreur", str(e))
            return

        try:
            room = Room(room_id, room_type, capacity)
            self.db.list_rooms.add_room(room)
            messagebox.showinfo("Succès", f"Salle {room.nom} créée")
            self._annuler()
        except ErrorRoom as e:
            messagebox.showerror("Erreur", str(e))

    def _annuler(self):
        """Reboot the form"""
        self.id_entry.delete(0, "end")
        self.type_menu.set("Standard")
        self.capacity_entry.delete(0, "end")
