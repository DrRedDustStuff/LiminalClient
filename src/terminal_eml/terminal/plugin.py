from types import ModuleType
from typing import Self, Any
import os

class Plugin:
    def __init__(self, main, plugins:list, display_name:str, id:str) -> None:
        self.main = main
        self.plugins = plugins
        self.display_name = display_name
        self.id = id.lower()
    
    # main initialization function (should return nothing)
    def initialize(self, *args, **kwargs):
        return self

import importlib
import sys
import importlib.util

def load_plugin(plugin:str, package:str):
    return importlib.import_module(plugin, package)

def reload_plugin(plugin:ModuleType):
    return importlib.reload(plugin)

def load_plugins(plugins_directory: str = "files/plugins") -> list[tuple[ModuleType, Any]]:
    plugins: list[tuple[ModuleType, Any]] = []

    plugins_path = os.path.abspath(plugins_directory)
    if not os.path.isdir(plugins_path):
        print(f"[Plugins] No plugins directory found at {plugins_path}")
        return plugins

    for entry in os.listdir(plugins_path):
        full_path = os.path.join(plugins_path, entry)

        # Skip junk
        if entry in {"__pycache__", "__init__.py"}:
            continue

        # Case 1: plugin is a folder with __init__.py
        if os.path.isdir(full_path) and os.path.isfile(os.path.join(full_path, "__init__.py")):
            module_name = entry
            module_path = os.path.join(full_path, "__init__.py")

        # Case 2: plugin is a single .py file
        elif entry.endswith(".py"):
            module_name = entry[:-3]
            module_path = full_path
        else:
            continue

        print(f"[Plugins] loading: {module_name}")

        try:
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = module
                spec.loader.exec_module(module)
                plugins.append((module, spec))
        except Exception as e:
            print(f"[Plugins] Failed to load {module_name}: {e}")

    return plugins