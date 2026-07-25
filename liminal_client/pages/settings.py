from .page import Page

from ..ui.ui_manager import WidgetManager
from customtkinter import CTkFont,DoubleVar
from ..ui.widgets import (
    Label,
    OptionMenu,
    Frame,
    Slider,
)
from .. import sound

class Settings(Page):
    key = "liminal_client.settings.page"

    def widgets(self):
        header = Label(
            self,
            text="liminal_client.settings_header.label",
            font=CTkFont(None, 42, "bold"),
        ).pack(padx=20, pady=10)

        language_header = Label(
            self, text="liminal_client.lang_sett_header.label"
        ).pack(padx=10, pady=(10, 0))

        def _(value: str):
            WidgetManager.translate(WidgetManager.language_keys[value])

        language = (
            OptionMenu(self, 300, 32, values=["English", "Deutsch"], command=_)
            .pack(padx=10, pady=(0, 10))
            .is_literal(True)
        )

        sound_category = Frame(self, border_width=2, corner_radius=8).pack(
            padx=0, pady=5, fill="x"
        )
        sound_category.pack_propagate(False)

        def _(x: float):
            sound.notification_channel.set_volume(x / 100)

        notification_volume = Slider(
            sound_category,
            border_width=2,
            width=400,
            from_=0,
            to=100,
            number_of_steps=100,
            command=_,
            variable=DoubleVar(value=sound.notification_channel.get_volume() * 100),
        ).pack(padx=25, pady=10, anchor="w")