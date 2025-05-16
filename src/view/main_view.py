import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar
import datetime
from reserve_view import ReserveView
from src.view.add_client_view import AddClientView
from src.view.display_view import DisplayView
from src.model.database import ListClients, ListRoom, ListReservation


class HomeScreen(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.clients_db = ListClients()
        self.rooms_db = ListRoom()
        self.reservations_db = ListReservation()

        self.title("MeetingPro - Accueil")
        self.geometry("1000x600")
        self.configure(fg_color="#1e1e2f")

        self.create_sidebar()
        self.create_main_content()
        self.update_clock()

    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=200, corner_radius=0, fg_color="#2c2f48"
        )
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar,
            text="Menu",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="white",
        ).pack(pady=20)

        self.btn_accueil = ctk.CTkButton(
            self.sidebar, text="Accueil", command=self.show_home
        )
        self.btn_accueil.pack(pady=10, fill="x", padx=10)

        self.btn_ajouter = ctk.CTkButton(
            self.sidebar, text="Ajouter", command=self.show_add
        )
        self.btn_ajouter.pack(pady=10, fill="x", padx=10)

        self.btn_reserver = ctk.CTkButton(
            self.sidebar, text="Réserver", command=self.show_reservation
        )
        self.btn_reserver.pack(pady=10, fill="x", padx=10)

        self.btn_afficher = ctk.CTkButton(
            self.sidebar, text="Afficher", command=self.show_display
        )
        self.btn_afficher.pack(pady=10, fill="x", padx=10)

    def create_main_content(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="#1e1e2f")
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.date_label = ctk.CTkLabel(
            self.main_frame,
            text=datetime.datetime.now().strftime("%A, %d %B %Y"),
            font=ctk.CTkFont(size=18),
        )
        self.date_label.pack(pady=10)

        self.clock_label = ctk.CTkLabel(
            self.main_frame, text="", font=ctk.CTkFont(size=16)
        )
        self.clock_label.pack()

        self.calendar = Calendar(
            self.main_frame, selectmode="day", date_pattern="yyyy-mm-dd"
        )
        self.calendar.pack(pady=20, expand=True, fill="both")

        self.info_label = ctk.CTkLabel(
            self.main_frame, text="Bienvenue dans MeetingPro", font=ctk.CTkFont(size=16)
        )
        self.info_label.pack(pady=10)

    def update_clock(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.configure(text=now)
        self.after(1000, self.update_clock)

    def show_home(self):
        messagebox.showinfo("Accueil", "Déjà sur la page d'accueil.")

    def show_add(self):
        messagebox.showinfo("Ajouter", "Accès à la section d'ajout.")

    def show_reservation(self):
        messagebox.showinfo("Réserver", "Accès à la réservation de salle.")

    def show_display(self):
        messagebox.showinfo("Afficher", "Affichage des données (clients, salles...).")


if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = HomeScreen()
    app.mainloop()
