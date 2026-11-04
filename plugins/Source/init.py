from blublib.plugin.plugin import Plugin
from blublib.resource import Identifier, _image_cache
from src.main import get_instance
from src.pages.settings import Settings
from customtkinter import CTkLabel

from typing import cast

class SourceInit(Plugin):
    def __init__(self) -> None:
        super().__init__()
        from . import console_commands
        console_commands.init()

    def initialize(self):
        instance = get_instance()
        instance.main_done_loading.bind(self.list_images)

    def list_images(self):
        instance = get_instance()
        settings = cast(Settings,instance.pages["liminal_client.settings"])
        debug_frame = settings.get_parent(Identifier.id("debug"))

        for path, img in _image_cache.items():
            CTkLabel(debug_frame, text=path, image=img, compound="left").pack(pady=4)

    def load(self): ...
    def unload(self): ...