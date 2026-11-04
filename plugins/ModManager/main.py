from tkinter import Event
from typing import Any

from src.main import LiminalClient
from src import main
from src import data
from blublib import resource

from blublib.plugin.plugin import Plugin
from blublib.ui.ui_manager import WidgetManager
from blublib.ui.widgets import (
    Button,
    Frame,
)
from blublib import resource

from .mod_display import ModDisplay
from . import loggers

from tkinter import filedialog

import os
import shutil
import json

import asyncio


class ModManager(Plugin):
    id = "mod_manager"
    version = "1.0"

    mod_pack = "default"

    def load(self):
        self.mods: list[ModDisplay] = []
        self.mods_data: dict[str, Any] = {}
        self.instance = main.get_instance()
        self.instance.main_done_loading.bind(self.done_loading)
        self.instance.all_widgets_loaded.bind(self.all_widgets_loaded)

    def done_loading(self):
        loggers.mod_manager.debug(
            "%s received that liminal client is done loading", self
        )
        self.load_mods_file()
        self.refresh_mods(None)

    def all_widgets_loaded(self):
        loggers.mod_manager.debug("%s received that all widgets were loaded", self)

    def load_mods(self):
        asyncio.run(self._load_mods())

    async def _load_mods(self):
        mod_display_queue: list = []
        async def load_mod(file: str):
            if not os.path.isfile(path + file):
                return
            if not (file.endswith(".pak") or file.endswith(".pak.dis")):
                return
            enabled = file.endswith(".pak")
            filename = file.removesuffix(".dis").removesuffix(".pak")
            if filename in self.mods_data["online"].keys():
                creator = "Unknown"
                name = "Unknown"
                id = -1
            elif filename in self.mods_data["direct"].keys():
                try:
                    creator = self.mods_data["direct"][filename]["creator"]
                    name = self.mods_data["direct"][filename]["name"]
                except KeyError as ke:
                    loggers.mod_manager.error("mods data is malformed: %s", str(ke))
                    creator = "Unknown"
                    name = filename
                    self.mods_data["direct"][filename].update(
                        {
                            "creator": creator,
                            "name": name,
                        }
                    )
                id = -1
            else:
                creator = "..."
                name = filename
                id = -128
            mod_display_queue.append((id,name,creator,enabled))

        path = data.etbPath + data.modsSuffix
        await asyncio.gather(*[load_mod(file) for file in os.listdir(path)])
        mod_pack_queue = []
        for id,name,creator,enabled in mod_display_queue:
            mod_pack_queue.append(self.add_mod_widget(id, name, creator, enabled))
            
        for mod_display in mod_pack_queue:
            mod_display.pack(padx=10, pady=4, fill="x")

    def refresh_mods(self, _):  # _ is event
        loggers.mod_manager.info("Refreshing mods")
        self.clear_mod_widgets()
        self.load_mods()
        h = len(self.mods) * (75 + 8)  # * (Mod display height + double pady)
        if h > 400:
            self.mods_frame.pack_propagate(True)
        else:
            self.mods_frame.pack_propagate(False)

    def upload_mod(self, _):
        initial_dir = os.path.realpath("C:/Users/" + data.login + "/Links/Downloads/")
        filepath = filedialog.askopenfilename(
            filetypes=(("PAK", "*.pak"),), title="Open pak file", initialdir=initial_dir
        )
        if filepath == "":
            return
        filename = os.path.basename(filepath)
        shutil.copyfile(filepath, data.etbPath + data.modsSuffix + filename)
        self.mods_data["direct"].update(
            {
                filename.removesuffix(".dis").removesuffix(".pak"): {
                    "creator": "unknown",
                    "version": "unknown",
                    "name": filename.removesuffix(".dis").removesuffix(".pak"),
                }
            }
        )
        self.refresh_mods(None)

    def add_mod_widget(
        self,
        id: int = 0,
        name: str = "NAME",
        creator: str = "CREATOR",
        enabled: bool = True,
    ):
        mod_display = ModDisplay(
            self, self.instance.main_frame.mods_frame, id, name, creator, enabled
        )
        self.mods.append(mod_display)
        return mod_display

    def clear_mod_widgets(self):
        for _ in self.mods.copy():
            self.mods.pop(0).destroy()

    def initialize(self):
        loggers.mod_manager.info("Initializing plugin %s", self.id)
        self.mods_frame: Frame = WidgetManager.get_widget_by_id(
            "liminal_client.mods.frame"
        )[0]
        self.refresh_mods_button: Button = WidgetManager.get_widget_by_id(
            "liminal_client.refresh_mods.button"
        )[0]
        self.refresh_mods_button.bind("<Button-1>", self.refresh_mods)

        self.upload_mod_button: Button = WidgetManager.get_widget_by_id(
            "liminal_client.upload_files.button"
        )[0]
        self.upload_mod_button.bind("<Button-1>", self.upload_mod)

    def unload(self):
        self.instance.all_widgets_loaded.unbind(self.all_widgets_loaded)
        self.instance.main_done_loading.unbind(self.done_loading)

        self.save_mods_file()

    def load_mods_file(self):
        loggers.mod_manager.info("Loading mod data file")
        if not "direct" in self.mods_data.keys():
            self.mods_data.update({"direct": {}})
        if not "online" in self.mods_data.keys():
            self.mods_data.update({"online": {}})
        if not os.path.exists(resource.datapath("_mods.json")):
            loggers.mod_manager.error("mod data file does not exist.")
            return
        with open(resource.datapath("_mods.json"), "r", encoding="utf-8") as rmdf:
            jsn: dict[str, list[dict[str, Any]]] = json.load(rmdf)
            self.mods_data.update(jsn)
            rmdf.close()

    def save_mods_file(self):
        loggers.mod_manager.info("Saving mod data file")
        with open(resource.datapath("_mods.json"), "w", encoding="utf-8") as wmdf:
            json.dump(self.mods_data, wmdf)
            wmdf.close()

    def represent(self) -> str:
        return "%s v:%s" % (super().represent(), self.version)
