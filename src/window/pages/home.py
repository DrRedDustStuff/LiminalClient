from typing import Any
import customtkinter as ctk
from .page import Page
from PIL import Image

import webbrowser

from window.translation_manager.label import TLabel
from window.translation_manager.translation_manager import TranslationManager

def get_image(file:str, size:tuple[int, int], ld:bool = False) -> ctk.CTkImage:
    """get image by file, file does not include .png
    <br>ld: has light and dark version, if true -light or -dark is appended *(Not implemented)"""
    return ctk.CTkImage(Image.open(f"files/images/{file}.png"), Image.open(f"files/images/{file}.png"), size)

class PHome(Page):
    def __init__(self, master: Any, translation_manager:TranslationManager):
        super().__init__(master, translation_manager)
        self.create_widgets()
    
    def create_widgets(self):
        self.l_window_label = TLabel(self, self.translation_manager, "home.header", font=self.style.font("header.h2"))
        self.l_window_label.place(relx=0.5,y=10, relwidth=0.8,relheight=0.2,anchor="n")
        
        self.b_discord_invite = ctk.CTkButton(self, 100, 100, 0, text="", image=get_image("discord-icon", (150,150)), command=lambda:webbrowser.open("https://discord.gg/EKYbRGR9hy"))
        self.b_discord_invite.place(relx=0.5,y=250, anchor="n")