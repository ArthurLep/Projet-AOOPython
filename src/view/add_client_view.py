import customtkinter as ctk
from tkinter import messagebox
from src.model.clients import Clients, ErrorClients


class AddClientView(ctk.CTkFrame):
    """View to add a new client."""

    def __init__(self, parent, db, on_success=None):
        super().__init__(parent)
        self.db = db
        self.on_success = on_success

        self.title_label = ctk.CTkLabel(
            self,
            text="Ajouter un nouveau client :",
            font=("Helvetica", 30),
            text_color="white",
        )
        self.title_label.pack(pady=(50, 20))

        self.lastname_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nom",
            justify="center",
            width=400,
            height=50,
            font=("Helvetica", 20),
        )
        self.firstname_entry = ctk.CTkEntry(
            self,
            placeholder_text="Prénom",
            justify="center",
            width=400,
            height=50,
            font=("Helvetica", 20),
        )
        self.email_entry = ctk.CTkEntry(
            self,
            placeholder_text="Adresse email",
            justify="center",
            width=400,
            height=50,
            font=("Helvetica", 20),
        )

        self.lastname_entry.pack(pady=(80, 5), padx=20)
        self.firstname_entry.pack(pady=(5, 5), padx=20)
        self.email_entry.pack(pady=(5, 50), padx=20)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20)

        self.validate_btn = ctk.CTkButton(
            btn_frame,
            text="Valider",
            command=self._valider,
            width=200,
            height=50,
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
            width=200,
            height=50,
            fg_color="red",
            hover_color="lightcoral",
            corner_radius=8,
            font=("Helvetica", 18),
        )
        self.erase_btn.pack(side="left", padx=(0, 0), pady=10)

    def _valider(self):
        """Validate the input fields and add a new client."""
        lastname = self.lastname_entry.get().strip()
        firstname = self.firstname_entry.get().strip()
        email = self.email_entry.get().strip()

        if not all([lastname, firstname, email]):
            messagebox.showerror("Erreur", "Tous les champs doivent être remplis.")
            return
        try:
            client = Clients(lastname, firstname, email)
            self.db.list_clients.add_client(client)
            messagebox.showinfo("Succès", f"Client {client.identity} créé")
            self._annuler()
            if self.on_success:
                self.on_success()
        except ErrorClients as e:
            messagebox.showerror("Erreur", str(e))

    def _annuler(self):
        """Clear the input fields."""
        self.lastname_entry.delete(0, "end")
        self.firstname_entry.delete(0, "end")
        self.email_entry.delete(0, "end")
