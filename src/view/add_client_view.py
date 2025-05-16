import customtkinter as ctk
import model.database as db


class AddClientView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db

        # Champs de formulaire
        self.lastname_entry = ctk.CTkEntry(self, placeholder_text="Nom")
        self.firstname_entry = ctk.CTkEntry(self, placeholder_text="Prénom")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")

        # Boutons
        self.validate_btn = ctk.CTkButton(self, text="Valider", command=self._valider)
        self.annuler_btn = ctk.CTkButton(self, text="Annuler", command=self._annuler)

        # Placement des éléments
        self.lastname_entry.pack(pady=10)
        self.firstname_entry.pack(pady=10)
        self.email_entry.pack(pady=10)
        self.validate_btn.pack(side="right", padx=5)
        self.annuler_btn.pack(side="left", padx=5)

    def _valider(self):
        """Appelle la méthode d'ajout de la Database"""
        lastname = self.lastname_entry.get()
        firstname = self.firstname_entry.get()
        email = self.email_entry.get()

        if lastname and firstname and email:
            self.db.add_client(lastname, firstname, email)

    def _annuler(self):
        """Réinitialise les champs"""
        self.lastname_entry.delete(0, "end")
        self.firstname_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
