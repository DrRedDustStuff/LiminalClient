import window
import customtkinter as ctk

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")

if __name__ == "__main__":
    app = window.main.Main()
    app.mainloop()
    print("Closing...\nSaving data")
    app.settings.save()

# src/main.py
# This file is the main entry point for the Neo-EML application.