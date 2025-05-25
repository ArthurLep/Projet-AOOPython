import customtkinter as ctk
from tkinter import ttk


class DisplayListRoom(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.rooms_tree = None
        self.room_search = None
        self.create_rooms_tab()

    def create_rooms_tab(self):
        """Display rooms tab"""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(tab, text="Salles")

        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        columns = ("ID", "Type", "Capacité")
        self.rooms_tree = ttk.Treeview(tab, columns=columns, show="headings")

        for col in columns:
            self.rooms_tree.heading(col, text=col)
            self.rooms_tree.column(col, width=150)

        vsb = ttk.Scrollbar(tab, orient="vertical", command=self.rooms_tree.yview)
        self.rooms_tree.configure(yscrollcommand=vsb.set)

        self.rooms_tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        refresh_btn = ctk.CTkButton(tab, text="🔄 Actualiser", command=self.load_rooms)
        refresh_btn.grid(row=1, column=0, pady=5)

        self.load_rooms()

    def load_rooms(self):
        """Charge la liste des salles dans le tableau"""
        self.rooms_tree.delete(*self.rooms_tree.get_children())
        for salle in self.db.list_rooms.rooms:
            self.rooms_tree.insert(
                "", "end", values=(salle.nom, salle.type, salle.capacity)
            )

    def load_rooms_list(self):
        """Met à jour la liste déroulante des salles (si utilisée ailleurs)"""
        if self.room_search:
            salles = [f"{s.type} ({s.nom})" for s in self.db.list_rooms.rooms]
            self.room_search.configure(values=salles)
