from typing import Any
import customtkinter as ctk
from window.mod_manager.mod import Mod

class PModpage(ctk.CTkFrame):
    def __init__(self, master: Any, mod:Mod):
        super().__init__(master, corner_radius=10)
        self.create_widgets(mod)
    
    def create_widgets(self, mod:Mod | None = None):
        self.l_window_label = ctk.CTkLabel(self, text="Modpage")
        if mod:
            self.l_window_label.configure(False, text="Modpage of "+mod.name)
        self.l_window_label.place(relx=0,rely=0, relwidth=1,relheight=1)