# main_view.py
import customtkinter as ctk
from tkinter import ttk
from View.add_client_view import AddClientView
from Model import database as db_module


class MainView(ctk.CTk):
    """Interface principale basique sans intégration modèle"""

    def __init__(self):
        super().__init__()
        self.title("MeetingPro - Interface")
        self.geometry("1000x600")

        self.database = db_module.ListClients()

        # Configuration du thème
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Configuration de la grille
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --------------- Barre latérale --------------- #
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")

        # Logo
        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="MeetingPro", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.pack(pady=40)

        # Boutons de navigation
        nav_buttons = [
            ("Accueil", self.show_accueil),
            ("Ajouter", self.show_ajouter),
            ("Réserver", self.show_reserver),
            ("Afficher", self.show_afficher),
        ]

        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar, text=text, command=command, corner_radius=8, height=40
            )
            btn.pack(pady=5, padx=10, fill="x")

        # --------------- Conteneur principal --------------- #
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Création des vues
        self.views = {}
        self.create_views()
        self.show_accueil()

    def create_views(self):
        # Vue Accueil
        accueil_frame = ctk.CTkFrame(self.main_container)
        self.views["accueil"] = accueil_frame
        ctk.CTkLabel(
            accueil_frame,
            text="Bienvenue sur MeetingPro\nSélectionnez une action dans la barre latérale",
            font=ctk.CTkFont(size=18),
        ).pack(pady=100)

        # Vue Ajouter
        add_client_view = AddClientView(self.main_container, self.database)
        self.views["ajouter"] = add_client_view
        # Ne pas ajouter de label ici, AddClientView a déjà ses widgets

        # Vue Réserver
        reserver_frame = ctk.CTkFrame(self.main_container)
        self.views["reserver"] = reserver_frame
        ctk.CTkLabel(
            reserver_frame,
            text="Section de réservation\nÀ implémenter",
            font=ctk.CTkFont(size=16),
        ).pack(pady=50)

        # Vue Afficher
        afficher_frame = ctk.CTkFrame(self.main_container)
        self.views["afficher"] = afficher_frame
        ctk.CTkLabel(
            afficher_frame,
            text="Section d'affichage des données\nÀ implémenter",
            font=ctk.CTkFont(size=16),
        ).pack(pady=50)

    def show_view(self, view_name):
        """Gère la navigation entre les vues"""
        for view in self.views.values():
            view.grid_forget()
        self.views[view_name].grid(row=0, column=0, sticky="nsew")

    def show_accueil(self):
        self.show_view("accueil")

    def show_ajouter(self):
        self.show_view("ajouter")

    def show_reserver(self):
        self.show_view("reserver")

    def show_afficher(self):
        self.show_view("afficher")


if __name__ == "__main__":
    app = MainView()
    app.mainloop()
