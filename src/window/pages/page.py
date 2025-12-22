import customtkinter as ctk

from typing import Any
from window.translation_manager import TranslationManager
from window.style_manager.tkstyle_reader import TKStyle

class Page(ctk.CTkFrame):
    def __init__(self, master, translation_manager: TranslationManager):
        super().__init__(master, corner_radius=0, bg_color=master._bg_color, fg_color=master._fg_color)
        self.main: Any = master.master.master
        self.translation_manager: TranslationManager = self.main.translation_manager
        self.style: TKStyle = self.main.style
    
    def place(self, **kwargs):
        return super().place(anchor="center",relx=0.5,rely=0.5,relwidth=0.98,relheight=0.98, **kwargs)
    