from typing import Any
import sys
import os
import json
import importlib
from .plugin import Plugin
from .plugin_event import PluginEvent
from blublib import log

dir = "./plugins/"
class _PluginManager:
    def __init__(self) -> None:
        sys.path.insert(0,dir)
        self.plugins: list[Plugin] = []

    def load(self):
        for folder in os.listdir(dir):
            if not os.path.isdir(dir+folder): continue
            if folder == "__pycache__": continue
            f = open(dir+folder+"/plugin.json", "r")
            data: dict[str,Any] = json.load(f)
            f.close()
            if "main" in data:
                plugin_module = importlib.import_module(folder+"."+data["main"][0], folder)
                self.plugins.append(getattr(plugin_module, data["main"][1])())

    def load_all(self):
        for p in self.plugins:
            log.info("> %s"%p.represent())
            p.load()

    def initialize_all(self):
        for p in self.plugins:
            p.initialize()

    def unload_all(self):
        for p in self.plugins:
            p.unload()

    def reload_all(self):
        PluginEvent.__check_empty__()
        for p in self.plugins:
            p.unload()
            p.load()

PluginManager = _PluginManager()