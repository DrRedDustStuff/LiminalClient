from typing import Any, Tuple

from .widgets import Frame, Label
from .ui_manager import WidgetManager

from typing import Any

from customtkinter import CTkImage, CTkFont

import customtkinter as ctk
from PIL.ImageTk import Image


class ModDisplay(Frame):
    def __init__(
        self,
        master: Any = None,
        mod_id: int = 0,
        mod_name: str = "<Mod>",
        mod_creator: str = "<Creator>",
    ):
        super().__init__(master, 200, 75)

        self._mid = mod_id

        image = Image.open("./resources/image/disc.png", "r")
        self.image = Label(
            self,
            text="",
            image=CTkImage(image, image, (64, 64)),
            fg_color="#4E4B22",
        ).tag("ModDisplayImage")
        self.image.pack(side="left", padx=4, pady=4).is_literal(True)

        fg = self.cget("fg_color")
        self.info = Frame(self, 300, height=1, fg_color=fg)
        self.infc_name = (
            Label(
                self.info,
                fg_color=fg,
                text=mod_name,
                font=CTkFont("Arial", 18, "bold"),
            )
            .id(f"<InfC-Name:{self._mid}>")
            .tag("ModDisplayText")
            .pack(side="top", anchor="w", expand=False)
            .is_literal(True)
        )
        self.infc_creator = (
            Label(
                self.info,
                fg_color=fg,
                text=mod_creator,
                font=CTkFont("Arial", 12),
            )
            .id(f"<InfC-Creator:{self._mid}>")
            .tag("ModDisplayText")
            .pack(side="bottom", anchor="w", expand=False)
            .is_literal(True)
        )

        self.info.pack(side="left", padx=4, pady=8, fill="y")
        self.info.pack_propagate(False)

        self.tag("ModDisplay")
        self.pack_propagate(False)

    def configure(self, require_redraw=False, **kwargs):
        if "image" in kwargs:
            self.image.configure(image=kwargs.pop("image"))
        if "name" in kwargs:
            self.infc_name.configure(text=kwargs.pop("name"))
        if "creator" in kwargs:
            self.infc_creator.configure(text=kwargs.pop("creator"))
        return super().configure(require_redraw, **kwargs)
