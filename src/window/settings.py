from typing import Any
import customtkinter as ctk

class PSettings(ctk.CTkFrame):
    def __init__(self, master: Any):
        super().__init__(master, corner_radius=10)
        self.create_widgets()
    
    def create_widgets(self):
        self.l_window_label = ctk.CTkLabel(self)
        self.l_window_label.place(relx=1,rely=1, relwidth=1,relheight=1)
    