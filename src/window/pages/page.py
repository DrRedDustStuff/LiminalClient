import customtkinter as ctk

from window.translation_manager import TranslationManager

class Page(ctk.CTkFrame):
    def __init__(self, master, translation_manager: TranslationManager):
        super().__init__(master, corner_radius=0, bg_color=master._bg_color, fg_color=master._fg_color)
        self.translation_manager = master.master.master.translation_manager
        self.font_style_manager = master.master.master.font_style_manager
    
    def place(self, **kwargs):
        return super().place(anchor="center",relx=0.5,rely=0.5,relwidth=0.98,relheight=0.98, **kwargs)
    