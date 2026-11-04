from blublib.ui.widgets import (
    Frame, 
    Label,
    Switch,
    Button,
)

from blublib import resource

from customtkinter import CTkImage, CTkFont

import customtkinter as ctk
from PIL.ImageTk import Image


def str_id(name: str, creator: str, id: int, v: str):
    return "<%s.%s.%s:%s>" % (name, creator, id, v)


def widgets(self: Frame, mod_name: str, mod_creator: str, mod_id: int):
    image = Image.open(resource.path("Source","image/disc.png"), "r")
    image = (
        Label(
            self,
            text="",
            image=CTkImage(image, image, (64, 64)),
            fg_color="#4E4B22",
        )
        .id(str_id(mod_name, mod_creator, mod_id, "Image"))
        .is_literal(True)
    )
    image.pack(side="left", padx=4, pady=4).is_literal(True)

    fg = self.cget("fg_color")
    info = Frame(self, 300, height=1, fg_color=fg)
    infc_name = (
        Label(
            info,
            fg_color=fg,
            text=mod_name,
            font=CTkFont("Arial", 18, "bold"),
        )
        .id(str_id(mod_name, mod_creator, mod_id, "Name"))
        .tag("ModDisplayText")
        .is_literal(True)
    )
    infc_creator = (
        Label(
            info,
            fg_color=fg,
            text=mod_creator,
            font=CTkFont("Arial", 12),
        )
        .id(str_id(mod_name, mod_creator, mod_id, "Creator"))
        .tag("ModDisplayText")
        .is_literal(True)
    )

    info.pack(side="left", padx=4, pady=8, fill="y")
    info.pack_propagate(False)

    management = Frame(
        self,
        200,
        75,
        fg_color=fg,
    )

    mng_delete = (
        Button(
            management,
            40,
            40,
            text="",
            image=resource.image("Source", "trash.png",(20,20)),
        )
        .id(str_id(mod_name,mod_creator,mod_id,"Delete"))
        .is_literal(True)
    )

    mng_enable = (
        Switch(
            management,
            20,
            text="",
        )
        .id(str_id(mod_name,mod_creator,mod_id,"Toggle"))
        .is_literal(True)
    )

    management.pack(side="right", padx=4, pady=8, fill="y")
    management.pack_propagate(False)

    self.tag("ModDisplay")
    self.pack_propagate(False)

    return (
        image, 
        infc_name.pack(side="top", anchor="w", expand=False), 
        infc_creator.pack(side="bottom", anchor="w", expand=False), 
        mng_delete.pack(side="right",anchor="e",padx=5), 
        mng_enable.pack(side="right",anchor="e",padx=5)
    )
