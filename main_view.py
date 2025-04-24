import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from tkcalendar import Calendar
import datetime, os
import json

# Users and reservations data files
users_file = "users.json"
reservations_file = "reservations.json"

# Saved users data
def load_users():
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    return {}

def save_users():
    with open(users_file, "w") as f:
        json.dump(users, f, indent=4)

users = load_users()

# Saved reservations data
def load_reservations():
    if os.path.exists(reservations_file):
        with open(reservations_file, "r") as f:
            return json.load(f)
    return {}

def save_reservations(data):
    with open(reservations_file, "w") as f:
        json.dump(data, f, indent=4)

# Welcome page : Login and Sign Up
class WelcomePage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MeetingPro - Welcome")
        self.geometry("1100x580")

        main_frame = ctk.CTkFrame(self, corner_radius=20, border_color="black", border_width=2)
        main_frame.pack(expand=True, padx=40, pady=40, fill="both")
        main_frame.columnconfigure((0, 1), weight=1)

        login_frame = ctk.CTkFrame(main_frame, fg_color="gray9", corner_radius=20)
        login_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")

        ctk.CTkLabel(login_frame, text="Log In", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 10))
        self.login_role = ctk.CTkOptionMenu(login_frame, values=["client", "admin"])
        self.login_role.pack(pady=10)
        self.login_email = ctk.CTkEntry(login_frame, placeholder_text="Email")
        self.login_email.pack(pady=10)
        self.login_password = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*")
        self.login_password.pack(pady=10)
        self.show_password_login_var = ctk.BooleanVar(value=False)
        self.show_password_login_btn = ctk.CTkCheckBox(login_frame, text="Show Password", variable=self.show_password_login_var, command=self.toggle_password_visibility, corner_radius=36)
        self.show_password_login_btn.pack()
        ctk.CTkButton(login_frame, text="Log In", command=self.login_action).pack(pady=20)

        signin_frame = ctk.CTkFrame(main_frame, fg_color="gray9", corner_radius=20)
        signin_frame.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")

        ctk.CTkLabel(signin_frame, text="Sign Up", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 10))
        self.signup_role = ctk.CTkOptionMenu(signin_frame, values=["client", "admin"])
        self.signup_role.pack(pady=10)
        self.signup_first_name = ctk.CTkEntry(signin_frame, placeholder_text="First Name")
        self.signup_first_name.pack(pady=10)
        self.signup_last_name = ctk.CTkEntry(signin_frame, placeholder_text="Last Name")
        self.signup_last_name.pack(pady=10)
        self.signup_email = ctk.CTkEntry(signin_frame, placeholder_text="New Email")
        self.signup_email.pack(pady=10)
        self.signup_password = ctk.CTkEntry(signin_frame, placeholder_text="New Password", show="*")
        self.signup_password.pack(pady=10)
        self.show_password_signup_var = ctk.BooleanVar(value=False)
        self.show_password_signup_btn = ctk.CTkCheckBox(signin_frame, text="Show Password", variable=self.show_password_signup_var, command=self.toggle_signup_password_visibility, corner_radius=36)
        self.show_password_signup_btn.pack()
        ctk.CTkButton(signin_frame, text="Create Account", command=self.signup_action).pack(pady=20)

    def toggle_password_visibility(self):
        self.login_password.configure(show="" if self.show_password_login_var.get() else "*")

    def toggle_signup_password_visibility(self):
        self.signup_password.configure(show="" if self.show_password_signup_var.get() else "*")

    def login_action(self):
        email = self.login_email.get()
        password = self.login_password.get()
        role = self.login_role.get()

        if email in users and users[email]["Password"] == password:
            if users[email]["Role"] == role:
                self.destroy()
                if role == "admin":
                    AdminInterface().mainloop()
                else:
                    ClientInterface(email=email).mainloop()
            else:
                messagebox.showerror("Role Error", "Incorrect role selected.")
        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def signup_action(self):
        first = self.signup_first_name.get()
        last = self.signup_last_name.get()
        email = self.signup_email.get()
        pwd = self.signup_password.get()
        role = self.signup_role.get()

        if not all([first, last, email, pwd]):
            return messagebox.showwarning("Sign Up", "Please fill all fields.")

        if email in users:
            return messagebox.showwarning("Sign Up", "Email already exists.")

        users[email] = {
            "First Name": first,
            "Last Name": last,
            "Password": pwd,
            "Role": role
        }
        save_users()
        messagebox.showinfo("Success", "Account created successfully.")
        self.destroy()
        if role == "admin":
            AdminInterface().mainloop()
        else:
            ClientInterface(email=email).mainloop()

# Client interface
class ClientInterface(ctk.CTk):
    def __init__(self, email):
        super().__init__()
        self.title("Client Dashboard")
        self.geometry("1025x700")
        self.email = email
        self.configure(fg_color="#1e1e2f")
        self.current_font_size = 16

        self.first_name = users[email]["First Name"]
        self.last_name = users[email]["Last Name"]

        self.set_font(self.current_font_size)

        self.grid_columnconfigure(0, weight=0)  # sidebar
        self.grid_columnconfigure(1, weight=1)  # main area
        self.grid_rowconfigure(0, weight=1)

        # ---------------- Sidebar ---------------- #
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#2c2f48")
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # profile picture
        self.profile_image_path = "default_profile.png"
        self.profile_image = self.load_profile_image(self.profile_image_path)
        self.profile_button = ctk.CTkButton(self.sidebar, image=self.profile_image, text="", width=100, height=100, command=self.change_profile_picture)
        self.profile_button.grid(row=0, column=0, pady=20, padx=10)

        # user name
        self.name_label = ctk.CTkLabel(self.sidebar, text=f"{self.first_name} {self.last_name}", font=ctk.CTkFont(size=16, weight="bold"))
        self.name_label.grid(row=1, column=0, pady=5)

        # Appearance mode
        ctk.CTkLabel(self.sidebar, text="Mode apparence", anchor="w").grid(row=2, column=0, pady=(20, 0), padx=10, sticky="w")
        self.appearance_menu = ctk.CTkOptionMenu(self.sidebar, values=["Light", "Dark", "System"], command=self.change_appearance)
        self.appearance_menu.set("System")
        self.appearance_menu.grid(row=3, column=0, padx=10, pady=5)

        # Font size
        ctk.CTkLabel(self.sidebar, text="Taille de police", anchor="w").grid(row=4, column=0, pady=(20, 0), padx=10, sticky="w")
        self.scale_menu = ctk.CTkOptionMenu(self.sidebar, values=["80%", "100%", "120%"], command=self.change_scale)
        self.scale_menu.set("100%")
        self.scale_menu.grid(row=5, column=0, padx=10, pady=5)

        # Logout button
        ctk.CTkButton(self.sidebar, text="Déconnexion", fg_color="#f97316", command=self.logout).grid(row=6, column=0, pady=30, padx=10)

        # --------------- Main Area ---------------- #
        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#1e1e2f")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=1)

        # Contenu exemple
        now = datetime.datetime.now()
        self.date_label = ctk.CTkLabel(self.main_frame, text=now.strftime("%A, %d %B %Y"), font=ctk.CTkFont(size=self.current_font_size))
        self.date_label.grid(row=0, column=0, pady=20)

        self.clock_label = ctk.CTkLabel(self.main_frame, text="", font=ctk.CTkFont(size=self.current_font_size - 2))
        self.clock_label.grid(row=1, column=0, pady=5)
        self.update_clock()

        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.grid(row=2, column=0, pady=20)

        self.reserve_button = ctk.CTkButton(self.button_frame, text="Reservations", width=150, command=self.reserve_action)
        self.reserve_button.grid(row=0, column=0, padx=10)

        self.view_res_button = ctk.CTkButton(self.button_frame, text="View reservations", width=180, command=self.view_reservations_action)
        self.view_res_button.grid(row=0, column=1, padx=10)

        self.calendar_frame = ctk.CTkFrame(self.main_frame)
        self.calendar_frame.grid(row=3, column=0, sticky="ew", padx=20, pady=20)

        self.calendar = Calendar(self.calendar_frame, selectmode='day', date_pattern='yyyy-mm-dd')
        self.calendar.pack(expand=True, fill="both")

    def update_clock(self):
        now = datetime.datetime.now().strftime("%H:%M:%S")
        self.clock_label.configure(text=now)
        self.after(1000, self.update_clock)

    def set_font(self, size):
        self.current_font_size = size

    def change_appearance(self, mode):
        ctk.set_appearance_mode(mode)

    def change_scale(self, value):
        scale_percent = int(value.strip('%'))
        font_size = int(16 * (scale_percent / 100))
        self.set_font(font_size)
        self.date_label.configure(font=ctk.CTkFont(size=font_size))
        self.clock_label.configure(font=ctk.CTkFont(size=font_size - 2))

    def load_profile_image(self, path):
        if os.path.exists(path):
            image = Image.open(path).resize((100, 100))
        else:
            image = Image.new("RGB", (100, 100), "gray")
        return ctk.CTkImage(light_image=image, dark_image=image, size=(100, 100))

    def change_profile_picture(self):
        filepath = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if filepath:
            self.profile_image_path = filepath
            self.profile_image = self.load_profile_image(filepath)
            self.profile_button.configure(image=self.profile_image)
            
    def reserve_action(self):
        print("Réserver une nouvelle réservation")

    def view_reservations_action(self):
        print("Afficher les réservations de l'utilisateur")

    def logout(self):
        self.destroy()

# Admin interface
class AdminInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("800x500")
        ctk.CTkLabel(self, text="Welcome Admin", font=ctk.CTkFont(size=22)).pack(pady=40)

# Lancement de l'application
if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    WelcomePage().mainloop()