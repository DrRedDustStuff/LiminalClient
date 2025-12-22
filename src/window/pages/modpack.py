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

class PModpack(Page):
    def __init__(self, master, translation_manager:TranslationManager, load_mods:bool = True):
        super().__init__(master, translation_manager)
        self.m_master = master 
        self.create_widgets(master, load_mods)
    
    def create_widgets(self, master, load_mods):
        self.l_window_label = TLabel(self, self.translation_manager, "modpack.header", font=self.style.font("header.h2"))
        self.l_window_label.place(relx=0.5,y=10, relwidth=1,relheight=0.2,anchor="n")

        self.f_mod_hider = ctk.CTkFrame(self, 0,0, 0, bg_color="transparent", fg_color="transparent")
        self.f_mod_hider.place(x=0,rely=0.25, relwidth=1,relheight=0.75)

        if load_mods: self.load_mods
    
    def load_mods(self):
        self.f_mod_hider.lift()
        # start

        MCTk.ModDisplay(self, self.main.show_page, Mod(author="AUTHOR", mod_id="MODID", mod_name="MODNAME", description="YOYOYOYO", mod_binary=b"ada", dependencies=["sosossoososos"])).place(x=0,rely=0.25,relwidth=1) # type: ignore
        self.f_mod_hider.lift()

        # end
        self.after(100,self.f_mod_hider.lower)

    def reload_mods(self):
        print("Reloading Mods")
        self.load_mods()# temporary
        # TODO
        # - clear currently loaded mods
        # - render new loaded mods





# MattFor should un nest his code for better readability :)
# (functions, inverted if statements, ect.)