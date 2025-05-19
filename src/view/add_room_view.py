import customtkinter as ctk
from tkinter import messagebox
from Model.room import Room, ErrorRoom


class AddRoomView(ctk.CTkFrame):
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
        """Crée les éléments de l'interface"""
        # Titre
        ctk.CTkLabel(
            self,
            text="Ajouter une nouvelle salle",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).grid(row=0, column=0, pady=20)

        # ID Salle
        self.id_label = ctk.CTkLabel(self, text="ID de la salle :")
        self.id_label.grid(row=1, column=0, padx=20, sticky="w")
        self.id_entry = ctk.CTkEntry(self, placeholder_text="Ex: S1, CONF-101...")
        self.id_entry.grid(row=1, column=0, padx=20, pady=5, sticky="e")

        # Type de salle
        self.type_label = ctk.CTkLabel(self, text="Type de salle :")
        self.type_label.grid(row=2, column=0, padx=20, sticky="w")
        self.type_var = ctk.StringVar(value="Standard")
        self.type_menu = ctk.CTkComboBox(
            self,
            variable=self.type_var,
            values=["Standard", "Conférence", "Informatique"],
        )
        self.type_menu.grid(row=2, column=0, padx=20, pady=5, sticky="e")

        # Capacité
        self.capacity_label = ctk.CTkLabel(self, text="Capacité :")
        self.capacity_label.grid(row=3, column=0, padx=20, sticky="w")
        self.capacity_entry = ctk.CTkEntry(self, placeholder_text="Nombre de places")
        self.capacity_entry.grid(row=3, column=0, padx=20, pady=5, sticky="e")

        # Boutons
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=4, column=0, pady=20, sticky="se")

        self.valider_btn = ctk.CTkButton(
            button_frame,
            text="Valider",
            command=self._valider,
            fg_color="#2ecc71",
            hover_color="#27ae60",
        )
        self.valider_btn.pack(side="right", padx=10)

        self.annuler_btn = ctk.CTkButton(
            button_frame,
            text="Annuler",
            command=self._annuler,
            fg_color="#e74c3c",
            hover_color="#c0392b",
        )
        self.annuler_btn.pack(side="left", padx=10)

    def _valider(self):
        """Valide les informations saisies et ajoute la salle à la base de données"""
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
            self.db.list_room.append(room)
            messagebox.showinfo("Succès", f"Salle {room.identity} créée")
            self._annuler()
        except ErrorRoom as e:
            messagebox.showerror("Erreur", str(e))

    def _annuler(self):
        """Réinitialise le formulaire"""
        self.id_entry.delete(0, "end")
        self.type_menu.set("Standard")
        self.capacity_entry.delete(0, "end")
