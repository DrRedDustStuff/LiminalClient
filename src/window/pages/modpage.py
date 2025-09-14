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
    def __init__(self, master: Any, translation_manager, mod:Mod):
        super().__init__(master, translation_manager)
        self.create_widgets(mod)
    
    def create_widgets(self, mod:Mod | None = None):
        md = mistune.create_markdown(renderer="ast")
        ast = md.read(join(dirname(getcwd()), "test.md"))[0]
        if isinstance(ast, list):
            self.md_display = CTkCreator(self, ast)
            self.md_display.place(relx=0.5,rely=0.5,relwidth=1,relheight=1,anchor="center")