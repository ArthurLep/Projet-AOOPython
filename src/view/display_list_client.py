import customtkinter as ctk
from tkinter import ttk


class DisplayListClient(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.clients_tree = None
        self.client_search = None
        self.create_clients_tab()

    def create_clients_tab(self):
        # creation of the notebook
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        # Creation of the client widget
        tab = ctk.CTkFrame(self.notebook, fg_color="transparent")
        self.notebook.add(tab, text=" Liste des clients :")

        tab.grid_rowconfigure(0, weight=1)
        tab.grid_rowconfigure(1, weight=0)
        tab.grid_columnconfigure(0, weight=1)

        # Treeview to display the client list
        columns = ("ID", "Nom", "Prénom", "Email")
        self.clients_tree = ttk.Treeview(
            tab, columns=columns, show="headings", selectmode="browse"
        )

        for col in columns:
            self.clients_tree.heading(col, text=col)
            self.clients_tree.column(col, width=200)

        vsb = ttk.Scrollbar(tab, orient="vertical", command=self.clients_tree.yview)
        self.clients_tree.configure(yscrollcommand=vsb.set)

        self.clients_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        refresh_btn = ctk.CTkButton(
            tab, text="🔄 Actualiser", command=self.load_clients, width=100
        )
        refresh_btn.grid(row=1, column=0, pady=5)

        self.load_clients()

    def load_clients(self):
        """Charge the client list in the treeview"""
        self.clients_tree.delete(*self.clients_tree.get_children())
        for client in self.db.list_clients.clients:
            self.clients_tree.insert(
                "",
                "end",
                values=(
                    client.identity,
                    client.LastName,
                    client.FirstName,
                    client.mail,
                ),
            )

    def load_clients_list(self):
        """Update the clients scrollbar"""
        if self.client_search:
            clients = [
                f"{c.FirstName} {c.LastName} ({c.identity})"
                for c in self.db.list_clients.list_client
            ]
            self.client_search.configure(values=clients)
