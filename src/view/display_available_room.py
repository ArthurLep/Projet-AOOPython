import customtkinter as ctk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, time


class DisplayAvailableRoom(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.start_date = None
        self.end_date = None
        self.start_time_entry = None
        self.end_time_entry = None
        self.availability_tree = None
        self.create_availability_tab()

    def create_availability_tab(self):
        """Availability research widger"""
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        tab = ctk.CTkFrame(self.notebook)
        self.notebook.add(tab, text="Disponibilités")

        tab.grid_rowconfigure(0, weight=1)
        tab.grid_columnconfigure(0, weight=1)

        # date control
        date_frame = ctk.CTkFrame(tab, fg_color="transparent")
        date_frame.grid(row=0, column=0, pady=(0, 5), sticky="ew")

        label_debut = ctk.CTkLabel(date_frame, text="Début :", font=("Helvetica", 16))
        label_debut.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.start_date = DateEntry(
            date_frame, date_pattern="dd/mm/yyyy", locale="fr_FR", width=40
        )
        self.start_date.grid(row=0, column=1, padx=5, pady=5)

        label_start_time = ctk.CTkLabel(
            date_frame,
            text="Heure (HH:MM) :",
            font=("Helvetica", 14),
        )
        label_start_time.grid(row=0, column=2, padx=5, pady=5)

        self.start_time_entry = ctk.CTkEntry(date_frame, width=80)
        self.start_time_entry.insert(0, "08:00")
        self.start_time_entry.grid(row=0, column=3, padx=5, pady=5)

        label_fin = ctk.CTkLabel(date_frame, text="Fin :", font=("Helvetica", 16))
        label_fin.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.end_date = DateEntry(
            date_frame, date_pattern="dd/mm/yyyy", locale="fr_FR", width=40
        )
        self.end_date.grid(row=1, column=1, padx=5, pady=5)

        label_end_time = ctk.CTkLabel(
            date_frame,
            text="Heure (HH:MM)",
            font=("Helvetica", 14),
        )
        label_end_time.grid(row=1, column=2, padx=5, pady=5)

        self.end_time_entry = ctk.CTkEntry(date_frame, width=80)
        self.end_time_entry.insert(0, "18:00")
        self.end_time_entry.grid(row=1, column=3, padx=5, pady=5)

        search_btn = ctk.CTkButton(
            date_frame,
            text="🔍 Rechercher",
            font=("Helvetica", 13),
            command=self.check_availability,
        )
        search_btn.grid(row=0, column=4, rowspan=2, padx=10, pady=5)

        # Result Table
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
        """Verify availability and display results"""
        try:
            start_hour, start_minute = map(
                int, self.start_time_entry.get().strip().split(":")
            )
            end_hour, end_minute = map(
                int, self.end_time_entry.get().strip().split(":")
            )
            debut = datetime.combine(
                self.start_date.get_date(), time(start_hour, start_minute)
            )
            fin = datetime.combine(self.end_date.get_date(), time(end_hour, end_minute))
        except ValueError:
            messagebox.showerror(
                "Erreur de saisie", "Veuillez entrer l'heure au format HH:MM."
            )
            return

        if debut >= fin:
            messagebox.showerror(
                "Erreur de période",
                "La date/heure de début doit précéder la date/heure de fin.",
            )
            return

        salles = self.db.list_available_rooms_on_period(debut, fin)

        self.availability_tree.delete(*self.availability_tree.get_children())
        for salle in salles:
            self.availability_tree.insert(
                "", "end", values=(salle.nom, salle.type, salle.capacity)
            )
