from src.view.main_view import HomeScreen
import customtkinter as ctk

if __name__ == "__main__":
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    # Initialisation de l'application
    app = HomeScreen()
    app.mainloop()
