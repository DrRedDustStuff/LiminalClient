from typing import Literal

class Mod:
    def __init__(self, name: str = "", author: str = "", dependencies: list[str] | None = None) -> None:
        # mod name
        self.name = name
        # mod author
        self.author = author
        
        self.has_dependencies = dependencies != None
        # list of mod names
        self.dependencies: list[str] | Literal["No Dependencies"] = dependencies if (self.has_dependencies and dependencies) else "No Dependencies"
    
    def _add_dependency(self, dependency:str):
        if not self.has_dependencies:
            self.has_dependencies = True
            self.dependencies = []
        self.dependencies.append(dependency) # type: ignore #, ignore the warning.

def mod_from_json(jsn:dict[str, str | list[str]]) -> Mod:
    """creates a Mod class from json data"""
    return Mod(jsn["name"],jsn["author"],jsn.get("dependencies")) # type: ignore ## str | list[str] error ##
    
    
class ModManager:
    def __init__(self, path:str|None = None) -> None:
        self.path: str
        if path: self.path = path
        else:    self.path = ""
        self.modpack:list[Mod] = [] # list of all mods.
    
    def _add_mod(self, mod:Mod):
        self.modpack.append(mod)