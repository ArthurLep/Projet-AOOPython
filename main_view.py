import tkinter as tk
from tkinter import ttk
import time

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Meeting Room Booking System")
        self.geometry("1024x640")
        self.create_widgets()
        self.update_time()  # Démarre la mise à jour de l'heure dès l'initialisation

    def create_widgets(self):
        label = ttk.Label(self, text="Welcome to MeetingPro !", font=("Impact", 35))
        label.pack(pady=20)

        # Espace Clients
        client_frame = ttk.LabelFrame(self, text="Client Area", padding="10")
        client_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        btn_client = ttk.Button(client_frame, text="Access Customer Options", command=self.open_client_interface)
        btn_client.pack(pady=5)

        # Espace Administratif
        admin_frame = ttk.LabelFrame(self, text="Administrative Area", padding="10")
        admin_frame.pack(fill="both", expand=True, padx=20, pady=10)

        btn_admin = ttk.Button(admin_frame, text="Access administrative options", command=self.open_admin_interface)
        btn_admin.pack(pady=5)

        # Display current time and date
        self.time_label = ttk.Label(self, font=("Helvetica", 14))
        self.time_label.pack(side="bottom", pady=10)

    def update_time(self):
        # Mise à jour de l'heure
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)  # Re-met à jour chaque seconde

    def open_admin_interface(self):
        # Ouvre une nouvelle fenêtre ou interface pour les options administratives
        admin_window = tk.Toplevel(self)
        admin_window.title("Admin Interface")
        admin_window.geometry("400x300")
        
        # Ajouter des options administratives
        admin_label = ttk.Label(admin_window, text="Choose an admin option", font=("Helvetica", 14))
        admin_label.pack(pady=20)

        btn_salle = ttk.Button(admin_window, text="Add a new room", command=self.add_room)
        btn_salle.pack(pady=5)

        btn_reservation = ttk.Button(admin_window, text="See the reservations", command=self.see_reservations)
        btn_reservation.pack(pady=5)

        btn_client = ttk.Button(admin_window, text="Add a new client", command=self.add_client)
        btn_client.pack(pady=5)
    
    def open_client_interface(self):
        # Ouvre une nouvelle fenêtre ou interface pour les options client
        client_window = tk.Toplevel(self)
        client_window.title("Client Interface")
        client_window.geometry("400x300")

        # Ajouter des options client
        client_label = ttk.Label(client_window, text="Choose a client option", font=("Helvetica", 14))
        client_label.pack(pady=20)

    def add_room(self):
        print("Add a new room")

    def see_reservations(self):
        print("See the reservations")

    def add_client(self):
        print("Add a new client")

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()