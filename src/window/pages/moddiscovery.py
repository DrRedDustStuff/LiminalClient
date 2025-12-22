# Misc imports
from typing import Any
# Required Libraries
from mod_manager import ctk as MCTk
from mod_manager.ctk import Mod
# ctk import
import customtkinter as ctk
from .page import Page

from window.translation_manager.label import TLabel
from window.translation_manager.translation_manager import TranslationManager

class PModDiscovery(Page):
    def __init__(self, master, translation_manager: TranslationManager):
        super().__init__(master, translation_manager)
        self.create_widgets()

    def create_widgets(self):
        self.l_header = TLabel(self, self.translation_manager, "moddiscovery.header", 0, 32, font=self.style.font("header.h2"))
        self.l_header.place(relx=0.5,y=12, relwidth=0.8, anchor="n")