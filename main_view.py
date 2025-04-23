import customtkinter as ctk
from tkinter import messagebox
import json
import os

# Config
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

# Load/save users
users_file = "users.json"
def load_users():
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    return {}

def save_users():
    with open(users_file, "w") as f:
        json.dump(users, f, indent=4)

users = load_users()

class WelcomePage(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MeetingPro - Welcome")
        self.geometry("1025x700")
        self.resizable(False, False)

        main_frame = ctk.CTkFrame(self, corner_radius=20)
        main_frame.pack(expand=True, padx=40, pady=40, fill="both")
        main_frame.columnconfigure((0, 1), weight=1)

        # Login Frame
        login_frame = ctk.CTkFrame(main_frame, corner_radius=20)
        login_frame.grid(row=0, column=0, padx=30, pady=30, sticky="nsew")

        ctk.CTkLabel(login_frame, text="Login", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(20, 10))
        self.login_role = ctk.CTkOptionMenu(login_frame, values=["client", "admin"])
        self.login_role.pack(pady=10)
        self.login_email = ctk.CTkEntry(login_frame, placeholder_text="Email")
        self.login_email.pack(pady=10)
        self.login_password = ctk.CTkEntry(login_frame, placeholder_text="Password", show="*")
        self.login_password.pack(pady=10)
        self.show_password_login_var = ctk.BooleanVar(value=False)
        self.show_password_login_btn = ctk.CTkCheckBox(login_frame, text="👁️", variable=self.show_password_login_var, command=self.toggle_password_visibility)
        self.show_password_login_btn.pack()
        ctk.CTkButton(login_frame, text="Login", command=self.login_action).pack(pady=20)

        # Signup Frame
        signin_frame = ctk.CTkFrame(main_frame, corner_radius=20)
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
        self.show_password_signup_btn = ctk.CTkCheckBox(signin_frame, text="👁️", variable=self.show_password_signup_var, command=self.toggle_signup_password_visibility)
        self.show_password_signup_btn.pack()
        ctk.CTkButton(signin_frame, text="Create Account", command=self.signup_action).pack(pady=20)

    def toggle_password_visibility(self):
        if self.show_password_login_var.get():
            self.login_password.configure(show="")  # Affiche le mot de passe
        else:
            self.login_password.configure(show="*")  # Cache le mot de passe

    def toggle_signup_password_visibility(self):
        if self.show_password_signup_var.get():
            self.signup_password.configure(show="")  # Affiche le mot de passe
        else:
            self.signup_password.configure(show="*")  # Cache le mot de passe    

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

class ClientInterface(ctk.CTk):
    def __init__(self, email):
        super().__init__()
        self.title("Client Dashboard")
        self.geometry("1025x700")
        self.email = email
        user_data = users.get(email, {})
        self.first_name = user_data.get("First Name", "")
        self.last_name = user_data.get("Last Name", "")

        header_frame = ctk.CTkFrame(self)
        header_frame.pack(pady=10, anchor="ne")
        ctk.CTkLabel(header_frame, text=f"{self.first_name} {self.last_name}", font=ctk.CTkFont(size=18)).pack(side="left")
        ctk.CTkLabel(header_frame, text="⚙️", font=ctk.CTkFont(size=28)).pack(side="left", padx=10)

        main_frame = ctk.CTkFrame(self, corner_radius=20)
        main_frame.pack(expand=True, padx=40, pady=40, fill="both")

        ctk.CTkButton(main_frame, text="Book a Room", command=self.book_room).pack(pady=20)
        ctk.CTkButton(main_frame, text="View Reservations", command=self.view_reservations).pack(pady=20)

    def book_room(self):
        messagebox.showinfo("Booking", "Booking feature coming soon!")

    def view_reservations(self):
        messagebox.showinfo("Reservations", "Reservation list coming soon!")

class AdminInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Admin Dashboard")
        self.geometry("800x500")
        ctk.CTkLabel(self, text="Welcome Admin", font=ctk.CTkFont(size=22)).pack(pady=40)

if __name__ == "__main__":
    WelcomePage().mainloop()