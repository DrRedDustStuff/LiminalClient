from tkinter import Event

from liminal_client.main import LiminalClient
from liminal_client import main
from liminal_client import log
from liminal_client import data
from liminal_client.plugin.plugin import Plugin
from liminal_client.ui.ui_manager import WidgetManager
from liminal_client.ui.widgets import (
    Button,
    Frame,
)

from .mod_display import ModDisplay

from tkinter import filedialog

import os
import shutil

class ModManager(Plugin):
    id = "mod_manager"
    version = "1.0"

    def load(self):
        self.mods: list[ModDisplay] = []
        self.instance = main.get_instance()
        self.instance.all_widgets_loaded.bind(self.all_widgets_loaded)

    def all_widgets_loaded(self):
        log.info("%s received that all widgets were loaded", self)

    def load_mods(self):
        path = data.etbPath+data.modsSuffix
        for file in os.listdir(path):
            if not os.path.isfile(path+file): continue
            if not (file.endswith(".pak") or file.endswith(".pak.dis")): continue
            enabled = file.endswith(".pak")
            name = file.removesuffix(".dis").removesuffix(".pak")
            creator = "Unknown"
            id = -1
            self.add_mod_widget(id,name,creator,enabled)

    def refresh_mods(self,_):
        log.info("Refreshing mods")
        self.clear_mod_widgets()
        self.load_mods()
        h = len(self.mods)*(75+8) # * (Mod display height + double pady)
        if h > 400:
            self.mods_frame.pack_propagate(True)
        else:
            self.mods_frame.pack_propagate(False)

    def upload_mod(self,_):
        filepath = filedialog.askopenfilename(
            filetypes=(("PAK", "*.pak"),), title="Open pak file", initialdir="$Downloads"
        )
        if filepath == "": return
        filename = os.path.basename(filepath)
        shutil.copyfile(filepath,data.etbPath+data.modsSuffix+filename)
        self.refresh_mods(None)

    def add_mod_widget(
        self,
        id: int = 0,
        name: str = "NAME",
        creator: str = "CREATOR",
        enabled: bool = True,
    ):
        mod_display = ModDisplay(self,self.instance.main_frame.mods_frame, id, name, creator, enabled)
        self.mods.append(mod_display)
        mod_display.pack(padx=10, pady=4, fill="x")
        
    def clear_mod_widgets(self):
        for _ in self.mods.copy():
            self.mods.pop(0).destroy()

    def initialize(self):
        log.info("Initializing plugin %s",self.id)
        self.mods_frame: Frame = WidgetManager.get_widget_by_id("liminal_client.mods.frame")[0]
        self.refresh_mods_button: Button = WidgetManager.get_widget_by_id("liminal_client.refresh_mods.button")[0]
        self.refresh_mods_button.bind("<Button-1>",self.refresh_mods)

        self.upload_mod_button: Button = WidgetManager.get_widget_by_id("liminal_client.upload_files.button")[0]
        self.upload_mod_button.bind("<Button-1>",self.upload_mod)

        self.refresh_mods(None)

    def unload(self):
        self.instance.all_widgets_loaded.unbind(self.all_widgets_loaded)

    def represent(self) -> str:
        return "%s v:%s"%(super().represent(),self.version)