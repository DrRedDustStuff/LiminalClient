from .page import Page

from blublib.ui.ui_manager import WidgetManager
from customtkinter import CTkFont,DoubleVar
from blublib.ui.widgets import (
    Label,
    Frame,
    Button,
    Entry,
)
from blublib import sound
from blublib import resource
from blublib.resource import Identifier
from .. import button_functions
from src import main

class Main(Page):
    key = Identifier.id("main")

    def widgets(self):
        self.instance = main.get_instance()

        header = Frame(self).pack(pady=(2, 0), fill="x", expand=True)
        run_game_button = Button(
            header,
            text=Identifier.id("run_game"),
            width=0,
            height=42,
            font=CTkFont(None, 16, "bold"),
            image=resource.image("Source", "round-play.png"),
            command=button_functions.run_game,
        ).pack(side="right", pady=12, padx=4)
        run_game_offline_button = Button(
            header,
            text=Identifier.id("run_game_offline"),
            width=0,
            height=42,
            font=CTkFont(None, 16, "bold"),
            image=resource.image("Source", "round-play.png"),
            command=button_functions.run_game_offline,
        ).pack(side="right", pady=12, padx=4)

        refresh_mods = Button(
            header,
            text=Identifier.id("refresh_mods"),
            width=0,
            height=38,
            font=CTkFont(None, 16, "bold"),
            image=resource.image("Source","refresh.png"),
        ).pack(side="left", pady=14, padx=4)

        mods_header = Label(
            self,
            text=Identifier.id("mods.header"),
            font=CTkFont(None, 42, "bold"),
        ).pack(padx=20, pady=10)
        hero = Frame(self).pack(fill="x", expand=True)

        upload_files = Button(
            hero,
            130,
            text=Identifier.id("upload_files"),
            image=resource.image("Source","folder-plus.png"),
        ).pack(side="right", padx=2)

        browse_content = Button(
            hero,
            140,
            text=Identifier.id("browse_content"),
            #state="disabled",
            image=resource.image("Source","compass.png"),
            command=lambda: self.instance.show_page(Identifier.id("mod_download"))
        ).pack(side="right", padx=2)

        mod_search = Entry(
            hero,
            placeholder_text=Identifier.id("mod_search"),  # , state="disabled"
        ).pack(side="left", fill="x", expand=True, padx=2)

        self.mods_frame = Frame(
            self,
            corner_radius=12,
            height=400,
            fg_color=WidgetManager.color("mods_frame"),
            border_width=3,
        ).pack(padx=2, pady=(18, 12), fill="both", expand=True).id(Identifier.id("mods"))

        self.footer = Frame(
            self, corner_radius=0, height=100, fg_color="transparent"
        ).pack(padx=0, pady=(12, 2), fill="x", expand=True)

        self._footer_left()
        self._footer_middle()
        self._footer_right()

    def _footer_left(self):
        self.footer_left = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=0, relwidth=(1 / 3), anchor="nw", relheight=1)

        self._footer_text(
            self.footer_left,
            Identifier.id("credit.head"),
            Identifier.id("credit.creator"),
            Identifier.id("."),
        )

    def _footer_middle(self):
        self.footer_middle = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=(1 / 3), relwidth=(1 / 3), anchor="nw", relheight=1)
        self._footer_text(
            self.footer_middle, 
            Identifier.id("about.head"), 
            Identifier.id(".")
        )

    def _footer_right(self):
        self.footer_right = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=(2 / 3), relwidth=(1 / 3), anchor="nw", relheight=1)
        self._footer_text(
            self.footer_right, 
            Identifier.id("help.head"), 
            Identifier.id(".")
        )

    def _footer_text(self, root, head: Identifier, *texts: Identifier):
        Label(root, text=head, font=CTkFont(None, 16, "bold")).pack(
            side="top", anchor="n", padx=10, pady=(10, 0)
        )
        for text in texts:
            Label(root, text=text).pack(side="top", anchor="n", padx=10, pady=(5, 0))