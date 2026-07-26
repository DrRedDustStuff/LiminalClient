from typing import Any

from liminal_client.ui.widgets import (
    Frame, 
    Label,
    Switch,
    Button,
)
from liminal_client.ui.ui_manager import WidgetManager
from liminal_client import data
from liminal_client import log

from customtkinter import BooleanVar

from ._mod_display import widgets, str_id

import os
import shutil

def prettify(state:bool):
    return "Enabled" if state else "Disabled"

class ModDisplay(Frame):
    def __init__(
        self,
        mod_manager: Any,
        master: Any = None,
        mod_id: int = 0,
        mod_name: str = "<Mod>",
        mod_creator: str = "<Creator>",
        mod_enabled: bool = True,
    ):
        super().__init__(master, 200, 75)

        self.manager = mod_manager

        self._mn = mod_name
        self._mc = mod_creator
        self._me = mod_enabled

        self._mid = mod_id
        widgets(self, mod_name, mod_creator, mod_id)

        self.image: Label = WidgetManager.get_widget_by_id(
            str_id(mod_name, mod_creator, mod_id, "Image")
        )[0]
        self.infc_name: Label = WidgetManager.get_widget_by_id(
            str_id(mod_name, mod_creator, mod_id, "Name")
        )[0]
        self.infc_creator: Label = WidgetManager.get_widget_by_id(
            str_id(mod_name, mod_creator, mod_id, "Creator")
        )[0]

        self.mng_delete: Button = WidgetManager.get_widget_by_id(
            str_id(mod_name,mod_creator,mod_id,"Delete")
        )[0]

        self.mng_delete.configure(command=self.delete)

        self.mng_enable: Switch = WidgetManager.get_widget_by_id(
            str_id(mod_name,mod_creator,mod_id,"Toggle")
        )[0]

        self.mng_enable.configure(command=self.toggle)
        self.mng_enable.configure(variable=BooleanVar(value=self._me))

    def get_postfix(self,state:bool):
        return ".pak" if state else ".pak.dis"

    def toggle(self):
        new = self.mng_enable.get() == 1
        log.info("Toggled mod %s from %s to %s",self._mn,prettify(self._me),prettify(new))
        os.rename(
            data.etbPath+data.modsSuffix+self._mn+self.get_postfix(self._me),
            data.etbPath+data.modsSuffix+self._mn+self.get_postfix(new),
        )
        self._me = new

    def delete(self):
        os.remove(data.etbPath+data.modsSuffix+self._mn+self.get_postfix(self._me))
        self.manager.refresh_mods(None)

    def configure(self, require_redraw=False, **kwargs):
        if "image" in kwargs:
            self.image.configure(image=kwargs.pop("image"))
        if "name" in kwargs:
            self.infc_name.configure(text=kwargs.pop("name"))
        if "creator" in kwargs:
            self.infc_creator.configure(text=kwargs.pop("creator"))
        return super().configure(require_redraw, **kwargs)
