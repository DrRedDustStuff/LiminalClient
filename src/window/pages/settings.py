# Misc Imports
from typing import Any
# ctk import
import customtkinter as ctk
from .page import Page

class PSettings(Page):
    def __init__(self, master: Any, translation_manager):
        super().__init__(master, translation_manager)
        self.create_widgets()
    
    def create_widgets(self):
        self.l_window_label = ctk.CTkLabel(self, text="Settings")
        self.l_window_label.place(relx=0.5,y=10, relwidth=0.8,relheight=0.2,anchor="n")
    