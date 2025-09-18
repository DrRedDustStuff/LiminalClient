# Misc Imports
from typing import Any
# ctk import
import customtkinter as ctk
from .page import Page

from window.translation_manager import TLabel, TButton
from window.translation_manager.translation_manager import TranslationManager

LANGMAP = {
    "English":"en",
    "Deutsch":"de"
}

class PSettings(Page):
    def __init__(self, master: Any, translation_manager:TranslationManager):
        super().__init__(master, translation_manager)
        self.create_widgets()
    
    def create_widgets(self):
        self.l_window_label = TLabel(self, self.translation_manager, "settings_page", font=self.font_style_manager("header.h2"))
        self.l_window_label.pack(side="top", padx=10,pady=10, fill="x")

        self.language = ctk.StringVar(self, "English", "language")
        self.language_setting = ctk.CTkOptionMenu(self, width=100,height=25, variable=self.language, values=["English", "Deutsch"],
                                 command=self.update_language)
        self.language_setting.pack(side="top", padx=10,pady=10, anchor="w")

        self.btn_apply = TButton(self, self.translation_manager, "apply_settings",
                                 command=self.apply_settings)
        self.btn_apply.pack(side="bottom", padx=20,pady=24, anchor="se")
    
    def update_language(self, lang:str):
        print(f"Updating language to {lang} ({LANGMAP.get(lang, "Undefined")})")
        self.translation_manager.switch_lang(LANGMAP.get(lang, "en"))

    def apply_settings(self):
        self.translation_manager.update_text_likes()
        self.main.settings.lang = self.translation_manager._lang