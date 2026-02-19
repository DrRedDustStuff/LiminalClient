from .. import data

import os, shutil
from pathlib import Path

class Mod:
    def __init__(self, path:Path) -> None:
        if not path.is_file(): raise Exception(f"path {path} is not a file")
        self.path = str(path).removesuffix(".dis").removesuffix(".pak")
        self.name = path.parts[-1].removesuffix(".dis").removesuffix(".pak")
        self.enabled = path.parts[-1][-4:] == ".pak"
        # ensure file is correctly named
        os.rename(path, data.game_folder+"/"+data.mod_path+"/"+self.name+(".pak" if self.enabled else ".dis"))

    def enable(self):
        if self.enabled: return
        if os.path.exists(self.path+".pak"): os.remove(self.path+".pak")
        os.rename(self.path+".dis", self.path+".pak")
        self.enabled = True

    def disable(self):
        if not self.enabled: return
        if os.path.exists(self.path+".dis"): os.remove(self.path+".dis")
        os.rename(self.path+".pak", self.path+".dis")
        self.enabled = False

    def toggle(self):
        if self.enabled:
            print(f"disabling mod {self.name}")
            self.disable()
        else:
            print(f"enabling mod {self.name}")
            self.enable()

    def delete(self):
        os.remove(self.path+(".pak" if self.enabled else ".dis"))

    def __str__(self) -> str:
        return f"<Mod name:{self.name} enabled:{self.enabled}>"