# Misc imports
from typing import Any
# Required Libraries
from mod_manager import ctk as MCTk
from mod_manager.ctk import Mod
# ctk import
import customtkinter as ctk
from .page import Page

class PModpack(Page):
    def __init__(self, master, translation_manager, load_mods:bool = True):
        super().__init__(master, translation_manager)
        self.m_master = master 
        self.create_widgets(master, load_mods)
    
    def create_widgets(self, master, load_mods):
        self.l_window_label = ctk.CTkLabel(self, text="Modpack")
        self.l_window_label.place(relx=0.5,y=10, relwidth=1,relheight=0.2,anchor="n")

        if load_mods:
            self.load_mods
    
    def load_mods(self):
        MCTk.ModDisplay(self, self.m_master.master.master.show_page, Mod("MODNAME", "MODAUTHOR")).place(x=0,rely=0.25,relwidth=1) # type: ignore

    def reload_mods(self):
        print("Reloading Mods")
        self.load_mods()# temporary
        # TODO
        # - clear currently loaded mods
        # - render new loaded mods