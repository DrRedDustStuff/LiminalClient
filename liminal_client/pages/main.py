from .page import Page

from ..ui.ui_manager import WidgetManager
from customtkinter import CTkFont,DoubleVar
from ..ui.widgets import (
    Label,
    Frame,
    Button,
    Entry,
)
from .. import sound
from .. import resource
from .. import button_functions

from ..ui.mod_display import ModDisplay

class Main(Page):
    key = "liminal_client.main.page"

    def widgets(self):
        header = Frame(self).pack(pady=(2, 0), fill="x", expand=True)
        run_game_button = Button(
            header,
            text="liminal_client.run_game.button",
            width=0,
            height=42,
            font=CTkFont(None, 16, "bold"),
            image=resource.image("round-play.png"),
            command=button_functions.run_game,
        ).pack(side="right", pady=12, padx=4)
        run_game_offline_button = Button(
            header,
            text="liminal_client.run_game_offline.button",
            width=0,
            height=42,
            font=CTkFont(None, 16, "bold"),
            image=resource.image("round-play.png"),
            command=button_functions.run_game_offline,
        ).pack(side="right", pady=12, padx=4)

        refresh_mods = Button(
            header,
            text="liminal_client.refresh_mods.button",
            width=0,
            height=38,
            font=CTkFont(None, 16, "bold"),
            image=resource.image("refresh.png"),
        ).pack(side="left", pady=14, padx=4)

        mods_header = Label(
            self,
            text="liminal_client.mods_header.label",
            font=CTkFont(None, 42, "bold"),
        ).pack(padx=20, pady=10)
        hero = Frame(self).pack(fill="x", expand=True)

        upload_files = Button(
            hero,
            130,
            text="liminal_client.upload_files.button",
            image=resource.image("folder-plus.png"),
        ).pack(side="right", padx=2)

        browse_content = Button(
            hero,
            140,
            text="liminal_client.browse_content.button",
            state="disabled",
            image=resource.image("compass.png"),
        ).pack(side="right", padx=2)

        mod_search = Entry(
            hero,
            placeholder_text="liminal_client.mod_search.entry",  # , state="disabled"
        ).pack(side="left", fill="x", expand=True, padx=2)

        self.mods_frame = Frame(
            self,
            corner_radius=12,
            height=400,
            fg_color=WidgetManager.color("mods_frame"),
            border_width=3,
        ).pack(padx=2, pady=(18, 12), fill="both", expand=True).id("liminal_client.mods.frame")

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
            "liminal_client.credit.head",
            "liminal_client.credit.creator",
            ".",
        )

    def _footer_middle(self):
        self.footer_middle = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=(1 / 3), relwidth=(1 / 3), anchor="nw", relheight=1)
        self._footer_text(self.footer_middle, "liminal_client.about.head", ".")

    def _footer_right(self):
        self.footer_right = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=(2 / 3), relwidth=(1 / 3), anchor="nw", relheight=1)
        self._footer_text(self.footer_right, "liminal_client.help.head", ".")

    def _footer_text(self, root, head: str, *texts: str):
        Label(root, text=head, font=CTkFont(None, 16, "bold")).pack(
            side="top", anchor="n", padx=10, pady=(10, 0)
        )
        for text in texts:
            Label(root, text=text).pack(side="top", anchor="n", padx=10, pady=(5, 0))