from types import ModuleType
from typing import Self, Any



import importlib
import pkgutil

def load_plugin(plugin:str):#, package:str):
    return importlib.import_module(plugin)

def load_plugins(directory_name:str):
    plugins: list[ModuleType] = []

    modules: ModuleType = importlib.import_module(directory_name)
    for loader, mname, is_pkg, in pkgutil.iter_modules(modules.__path__):
        print(f"[Plugins] loading: {mname}")

        full_name = f"{directory_name}.{mname}"
        plugins.append(load_plugin(full_name))
    
    return plugins