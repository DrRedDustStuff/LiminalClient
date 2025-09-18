from typing import Literal
from mdpackhandler import MDPackHandler

# pure container class
class Mod:
    def __init__(self, author:str, mod_id:str, mod_name:str, description:str, mod_binary:bytes, dependencies:list[str]) -> None:
        self.author = author
        self.mod_id = mod_id
        self.mod_name = mod_name
        self.description = description
        self.mod = mod_binary
        self.dependencies = dependencies

class ModManager:
    def __init__(self, mod_data_directory:str|None = None, path:str|None = None) -> None:
        self.path: str
        self.md_directory: str
        if not path: self.path = ""
        if not mod_data_directory: self.md_directory = ""
        self.modpack:list[Mod] = [] # list of all mods.
    
    def _add_mod(self, mod:Mod):
        self.modpack.append(mod)