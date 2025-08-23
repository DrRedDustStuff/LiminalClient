# Misc imports
from typing import Any
# Required Libraries
from mod_manager.mod import Mod
from MATC import CTkCreator
import mistune
# ctk import
import customtkinter as ctk
from .page import Page
from os import getcwd
from os.path import join, dirname

class PModpage(Page):
    def __init__(self, master: Any, mod:Mod):
        super().__init__(master)
        self.create_widgets(mod)
    
    def create_widgets(self, mod:Mod | None = None):
        self.l_window_label = ctk.CTkLabel(self, text="Modpage", font=ctk.CTkFont(None, 24, "bold"))
        if mod:
            self.l_window_label.configure(False, text="Modpage of "+mod.name)
        self.l_window_label.place(relx=0.5,y=10, relwidth=0.8,relheight=0.2,anchor="n")

        md = mistune.create_markdown(renderer="ast")
        ast = md.read(join(dirname(getcwd()), "test.md"))[0]
        if isinstance(ast, list):
            self.md_display = CTkCreator(self, ast)
            self.md_display.place(relx=0.5,rely=0.2,relwidth=0.9,relheight=0.6,anchor="n")