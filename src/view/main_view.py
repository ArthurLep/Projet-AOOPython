import customtkinter as ctk
from ..View.add_client_view import AddClientView
from ..View.add_room_view import AddRoomView
from ..Model.database import ListClients, Database
from ..View.reserve_view import ReserveView


class MainView(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MeetingPro - Interface")
        self.geometry("1000x600")

        self.database = Database()

        # Apparence
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        # Grille principale
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ---------------- Barre latérale ---------------- #
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.logo_label = ctk.CTkLabel(
            self.sidebar, text="MeetingPro", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.pack(pady=40)

        nav_buttons = [
            ("Accueil", self.show_accueil),
            ("Ajouter", self.show_ajouter_menu),
            ("Réserver", self.show_reserver),
            ("Afficher", self.show_afficher),
        ]

        for text, command in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar, text=text, command=command, corner_radius=8, height=40
            )
            btn.pack(pady=5, padx=10, fill="x")

        # ---------------- Conteneur central ---------------- #
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        # Dictionnaire des vues
        self.views = {}
        self.create_views()
        self.show_accueil()

    def create_views(self):
        # Vue Accueil
        accueil_frame = ctk.CTkFrame(self.main_container)
        ctk.CTkLabel(
            accueil_frame,
            text="Bienvenue sur MeetingPro\nSélectionnez une action dans la barre latérale",
            font=ctk.CTkFont(size=18),
            justify="center",
        ).pack(expand=True)
        self.views["accueil"] = accueil_frame

        # Vue menu "Ajouter"
        ajouter_menu = ctk.CTkFrame(self.main_container)
        ctk.CTkLabel(
            ajouter_menu, text="Que souhaitez-vous ajouter ?", font=ctk.CTkFont(size=18)
        ).pack(pady=40)

        btn_client = ctk.CTkButton(
            ajouter_menu, text="Ajouter un client", command=self.show_add_client
        )
        btn_client.pack(pady=10)

        btn_salle = ctk.CTkButton(
            ajouter_menu, text="Ajouter une salle", command=self.show_add_room
        )
        btn_salle.pack(pady=10)

        self.views["ajouter_menu"] = ajouter_menu

        # Vue Ajouter un client
        ajouter_client_frame = ctk.CTkFrame(self.main_container)
        self.add_client_view = AddClientView(ajouter_client_frame, self.database)
        self.add_client_view.pack(fill="both", expand=True)
        self.views["ajouter_client"] = ajouter_client_frame

        # Vue Ajouter une salle (à implémenter plus tard)
        ajouter_salle_frame = ctk.CTkFrame(self.main_container)
        self.add_room_view = AddRoomView(ajouter_salle_frame, self.database)
        self.add_room_view.pack(fill="both", expand=True)
        self.views["ajouter_salle"] = ajouter_salle_frame

        # Vue Réserver
        reserver_frame = ctk.CTkFrame(self.main_container)
        self.reserve_view = ReserveView(reserver_frame, self, self.database)
        self.reserve_view.pack(fill="both", expand=True)
        self.views["reserver"] = reserver_frame

        # Vue Afficher
        afficher_frame = ctk.CTkFrame(self.main_container)
        ctk.CTkLabel(
            afficher_frame,
            text="Affichage des données - à implémenter",
            font=ctk.CTkFont(size=16),
        ).pack(pady=100)
        self.views["afficher"] = afficher_frame

    def show_view(self, view_name):
        """Affiche une vue et masque les autres"""
        for view in self.views.values():
            view.grid_forget()
        self.views[view_name].grid(row=0, column=0, sticky="nsew")

    # Fonctions de navigation
    def show_accueil(self):
        self.show_view("accueil")

    def show_ajouter_menu(self):
        self.show_view("ajouter_menu")

    def show_add_client(self):
        self.show_view("ajouter_client")

    def show_add_room(self):
        self.show_view("ajouter_salle")

    def show_reserver(self):
        self.show_view("reserver")

    def show_afficher(self):
        self.show_view("afficher")


if __name__ == "__main__":
    app = MainView()
    app.mainloop()
