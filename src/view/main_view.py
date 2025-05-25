import customtkinter as ctk
from .add_client_view import AddClientView
from ..view.add_room_view import AddRoomView
from ..model.database import Database
from ..view.reserve_view import ReserveView
from ..view.display_list_client import DisplayListClient
from ..view.display_list_room import DisplayListRoom
from ..view.display_available_room import DisplayAvailableRoom
from ..view.display_reservation import DisplayReservation


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

        # View "Ajouter" Menu
        ajouter_menu = ctk.CTkFrame(self.main_container)
        ctk.CTkLabel(
            ajouter_menu, text="Que souhaitez-vous ajouter ?", font=ctk.CTkFont(size=30)
        ).pack(pady=40)

        btn_client = ctk.CTkButton(
            ajouter_menu, text="Ajouter un nouveau client", command=self.show_add_client
        )
        btn_client.pack(pady=10)

        btn_salle = ctk.CTkButton(
            ajouter_menu, text="Ajouter une nouvelle salle", command=self.show_add_room
        )
        btn_salle.pack(pady=10)

        self.views["ajouter_menu"] = ajouter_menu

        # Add Client View
        ajouter_client_frame = ctk.CTkFrame(self.main_container)
        self.add_client_view = AddClientView(
            ajouter_client_frame, self.database, on_success=self.show_accueil
        )
        self.add_client_view.pack(fill="both", expand=True)
        self.views["ajouter_client"] = ajouter_client_frame

        # Add Room View
        ajouter_salle_frame = ctk.CTkFrame(self.main_container)
        self.add_room_view = AddRoomView(ajouter_salle_frame, self.database)
        self.add_room_view.pack(fill="both", expand=True)
        self.views["ajouter_salle"] = ajouter_salle_frame

        # Reserve View
        reserver_frame = ctk.CTkFrame(self.main_container)
        self.reserve_view = ReserveView(reserver_frame, self, self.database)
        self.reserve_view.pack(fill="both", expand=True)
        self.views["reserver"] = reserver_frame

        # Display view
        display_frame = ctk.CTkFrame(self.main_container)
        display_frame.grid_rowconfigure(1, weight=1)
        display_frame.grid_columnconfigure(0, weight=1)

        buttons_frame = ctk.CTkFrame(display_frame)
        buttons_frame.grid(row=0, column=0, sticky="ew", pady=10, padx=10)

        content_frame = ctk.CTkFrame(display_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        self.current_display_view = None

        def clear_content():
            if self.current_display_view:
                self.current_display_view.pack_forget()
                self.current_display_view.destroy()
                self.current_display_view = None

        def show_clients():
            clear_content()
            self.current_display_view = DisplayListClient(content_frame, self.database)
            self.current_display_view.pack(fill="both", expand=True)

        def show_rooms():
            clear_content()
            self.current_display_view = DisplayListRoom(content_frame, self.database)
            self.current_display_view.pack(fill="both", expand=True)

        def show_available_rooms():
            clear_content()
            self.current_display_view = DisplayAvailableRoom(
                content_frame, self.database
            )
            self.current_display_view.pack(fill="both", expand=True)

        def show_reservations():
            clear_content()
            self.current_display_view = DisplayReservation(content_frame, self.database)
            self.current_display_view.pack(fill="both", expand=True)

        btn_clients = ctk.CTkButton(
            buttons_frame, text="Afficher liste client", command=show_clients
        )
        btn_salles = ctk.CTkButton(
            buttons_frame, text="Afficher liste salle", command=show_rooms
        )
        btn_salles_dispo = ctk.CTkButton(
            buttons_frame, text="Afficher salle dispo", command=show_available_rooms
        )
        btn_reserv_client = ctk.CTkButton(
            buttons_frame,
            text="Afficher réservation par client",
            command=show_reservations,
        )

        btn_clients.pack(side="left", padx=5)
        btn_salles.pack(side="left", padx=5)
        btn_salles_dispo.pack(side="left", padx=5)
        btn_reserv_client.pack(side="left", padx=5)

        show_clients()
        self.views["afficher"] = display_frame

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
        self.reserve_view.reset()
        self.show_view("reserver")

    def show_afficher(self):
        self.show_view("afficher")

    def show_confirmation(self):
        confirmation_window = ctk.CTkToplevel(self)
        confirmation_window.title("Confirmation de réservation")
        confirmation_window.geometry("300x150")

        label = ctk.CTkLabel(
            confirmation_window,
            text="Réservation confirmée !",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        label.pack(pady=30)

        btn_ok = ctk.CTkButton(
            confirmation_window, text="OK", command=confirmation_window.destroy
        )
        btn_ok.pack(pady=10)
