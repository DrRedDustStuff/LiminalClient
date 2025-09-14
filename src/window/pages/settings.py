# Misc Imports
from typing import Any
# ctk import
import customtkinter as ctk
from .page import Page

from window.translation_manager.label import TLabel
from window.translation_manager.translation_manager import TranslationManager

class PSettings(Page):
    def __init__(self, master: Any, translation_manager:TranslationManager):
        super().__init__(master, translation_manager)
        self.create_widgets()
    
    def create_widgets(self):
        self.l_window_label = TLabel(self, self.translation_manager, "settings_page", font=self.font_style_manager("header.h2"))
        self.l_window_label.place(relx=0.5,y=10, relwidth=0.8,relheight=0.2,anchor="n")
    