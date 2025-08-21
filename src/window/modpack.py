from typing import Any
import customtkinter as ctk

from window.mod_manager import ctk as MCTk
from window.mod_manager._ctk import Mod

class PModpack(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=10)
        self.create_widgets(master)
    
    def create_widgets(self, master):
        self.l_window_label = ctk.CTkLabel(self, text="Modpack")
        self.l_window_label.place(x=0,y=0, relwidth=1,relheight=0.2)

        MCTk.ModDisplay(self, master.master.master.show_tab, Mod("MODNAME", "MODAUTHOR")).place(x=0,rely=0.25,relwidth=1) # type: ignore
    