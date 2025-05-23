import customtkinter as ctk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime


class DisplayAvailableRoom(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.start_date = None
        self.end_date = None
        self.availability_tree = None
        self.create_availability_tab()

    def create_availability_tab(self):
        """Onglet de recherche de disponibilités"""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(tab, text="Disponibilités")

        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        # Contrôles de date
        date_frame = ctk.CTkFrame(tab, fg_color="transparent")
        date_frame.grid(row=0, column=0, pady=10, sticky="ew")

        ctk.CTkLabel(date_frame, text="Début :").pack(side="left", padx=5)
        self.start_date = DateEntry(
            date_frame, date_pattern="dd/mm/yyyy", locale="fr_FR"
        )
        self.start_date.pack(side="left", padx=5)

        ctk.CTkLabel(date_frame, text="Fin :").pack(side="left", padx=5)
        self.end_date = DateEntry(date_frame, date_pattern="dd/mm/yyyy", locale="fr_FR")
        self.end_date.pack(side="left", padx=5)

        search_btn = ctk.CTkButton(
            date_frame, text="🔍 Rechercher", command=self.check_availability
        )
        search_btn.pack(side="left", padx=10)

        # Tableau des résultats
        columns = ("ID Salle", "Type", "Capacité")
        self.availability_tree = ttk.Treeview(tab, columns=columns, show="headings")

        for col in columns:
            self.availability_tree.heading(col, text=col)
            self.availability_tree.column(col, width=150)

        vsb = ttk.Scrollbar(
            tab, orient="vertical", command=self.availability_tree.yview
        )
        self.availability_tree.configure(yscrollcommand=vsb.set)

        self.availability_tree.grid(row=1, column=0, sticky="nsew")
        vsb.grid(row=1, column=1, sticky="ns")

    def check_availability(self):
        """Vérifie les disponibilités et affiche les résultats"""
        debut = datetime.combine(self.start_date.get_date(), datetime.min.time())
        fin = datetime.combine(self.end_date.get_date(), datetime.min.time())

        salles = self.db.list_available_rooms(debut, fin)

        self.availability_tree.delete(*self.availability_tree.get_children())
        for salle in salles:
            self.availability_tree.insert(
                "", "end", values=(salle.nom, salle.type, salle.capacity)
            )
