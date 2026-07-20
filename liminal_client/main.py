from typing import Any

from customtkinter import CTk, CTkFont

from .ui.widgets import (
    Frame,
    ScrollableFrame,
    Label,
    Entry,
    Button,
)
from .ui.mod_display import ModDisplay
from .datafile import Datafile
from . import data, resource

from threading import Thread

import customtkinter as ctk


class LiminalClient:
    def load(self):
        data.initialize()
        self.ready = True

    def __init__(self) -> None:
        ctk.set_default_color_theme("./resources/theme.json")

        self.tk = CTk()
        self.tk.geometry(f"1200x800")
        self.tk.minsize(1200, 800)
        self.tk.resizable(True, True)

        self.ready = False
        self.load_thread = Thread(target=self.load, daemon=True)
        self.load_thread.start()

        self.tk.title("Liminal Client")

        self.widgets(self.tk)
        self.tk.mainloop()
        self.load_thread.join()

    def widgets(self, master):
        self.main_header = Label(
            master, text="Liminal Client", font=CTkFont(None, 30, "bold")
        ).place(y=4, x=100)

        self.version_label = Label(
            master,
            text_color="#969696",
            text=f"v:" + data.version(),
            font=CTkFont(None, 14, "normal", "italic"),
        ).place(y=12, x=300)

        self.main = Frame(master, corner_radius=24)
        self.main.place(x=30, y=50, relwidth=1, relheight=1)
        self.main_ = ScrollableFrame(
            self.main, corner_radius=0, fg_color=self.main.cget("fg_color")
        ).tag("main")
        self.main_.pack(padx=(15, 35), pady=(0, 60), fill="both", expand=True)

        root = self.main_

        self.main_frame(root)

    def main_frame(self, root: ScrollableFrame):
        self.header = Frame(root).pack(fill="x", expand=True)
        self.run_game_button = Button(
            self.header,
            text="Run Game",
            width=0,
            height=42,
            font=CTkFont(None, 16, "bold"),
            image=resource.image("round-play.png"),
        ).pack(side="right", pady=12, padx=4)

        self.mods_header = Label(
            root, text="Mods:", font=CTkFont(None, 42, "bold")
        ).pack(padx=20, pady=10)
        self.hero = Frame(root).pack(fill="x", expand=True)

        self.upload_files = Button(
            self.hero, 130, text="Upload files", image=resource.image("folder-plus.png")
        ).pack(side="right", padx=2)

        self.browse_content = Button(
            self.hero,
            140,
            text="Browse content",
            state="disabled",
            image=resource.image("compass.png"),
        ).pack(side="right", padx=2)

        self.mod_search = Entry(
            self.hero, placeholder_text="Search mods...", state="disabled"
        ).pack(side="left", fill="x", expand=True, padx=2)

        self.mods_frame = Frame(
            root, corner_radius=12, height=200, fg_color="#1B1B1B"
        ).pack(padx=2, pady=(18, 12), fill="both", expand=True)

        self.footer = Frame(
            root, corner_radius=0, height=100, fg_color="transparent"
        ).pack(padx=0, pady=(12, 2), fill="x", expand=True)

        self.footer_left = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=0, relwidth=(1 / 3), anchor="nw", relheight=1)

        self.footer_middle = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=(1 / 3), relwidth=(1 / 3), anchor="nw", relheight=1)

        self.footer_right = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=(2 / 3), relwidth=(1 / 3), anchor="nw", relheight=1)


def main():
    LiminalClient()
