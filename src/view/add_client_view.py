import customtkinter as ctk
from tkinter import messagebox
from src.Model.clients import Clients, ErrorClients


class AddClientView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db

        self.lastname_entry = ctk.CTkEntry(self, placeholder_text="Nom")
        self.firstname_entry = ctk.CTkEntry(self, placeholder_text="Prénom")
        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")

        self.validate_btn = ctk.CTkButton(self, text="Valider", command=self._valider)
        self.annuler_btn = ctk.CTkButton(self, text="Annuler", command=self._annuler)

        self.lastname_entry.pack(pady=10)
        self.firstname_entry.pack(pady=10)
        self.email_entry.pack(pady=10)
        self.validate_btn.pack(side="right", padx=5)
        self.annuler_btn.pack(side="left", padx=5)

    def _valider(self):
        lastname = self.lastname_entry.get().strip()
        firstname = self.firstname_entry.get().strip()
        email = self.email_entry.get().strip()

        if not all([lastname, firstname, email]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return
        try:
            client = Clients(lastname, firstname, email)
            self.db.add_client(client)
            messagebox.showinfo("Succès", f"Client {client.identity} créé")
            self._annuler()
        except ErrorClients as e:
            messagebox.showerror("Erreur", str(e))

    def _annuler(self):
        self.lastname_entry.delete(0, "end")
        self.firstname_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
