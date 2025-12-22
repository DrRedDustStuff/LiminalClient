

class Mod:
    def __init__(self, name:str, file:str, state:bool) -> None:
        self.name = name
        self.file = file
        self.state = state

    def set_state(self, new_state:bool):
        self.state = new_state
    
class ModKeeper:
    def __init__(self, folder:str) -> None:
        self.__folder__ = folder
        self.__mods__: list[Mod] = []
    
    def append(self, new:Mod):
        for m in self.__mods__:
            if m.name == new.name:
                #print("Mod already exists")
                return
        self.__mods__.append(new)
    
    def set_folder(self, new:str):
        self.__folder__ = new
    
    def __getitem__(self, i:str):
        for m in self.__mods__:
            if m.name == i:
                return m
        return None

    def __setitem__(self, i:str, v:Mod):
        for j,m in enumerate(self.__mods__):
            if not m.name == i: continue
            self.__mods__[j] = v