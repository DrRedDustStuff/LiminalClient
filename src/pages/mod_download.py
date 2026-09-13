from .page import Page

from blublib.ui.ui_manager import WidgetManager
from customtkinter import CTkFont,DoubleVar
from blublib.ui.widgets import (
    Label,
    OptionMenu,
    Frame,
    Slider,
)
from blublib.ui.labeled_slider import LabeledSlider
from blublib import sound
from blublib import resource
from blublib.resource import Identifier

from src import main

class ModDownload(Page):
    key = Identifier.id("mod_download")
    add_direct = False

    def __init__(self, parent):
        super().__init__(parent)
        self.instance = main.get_instance()

        self.instance.pages.update({(self.key.getNamespace() + "." + self.key.getPath()):self})

    def widgets(self):
        header = Label(
            self,
            text="liminal_client.mod_download.header.label",
            font=CTkFont(None, 42, "bold"),
        ).pack(padx=20, pady=10)