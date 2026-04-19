from .. import logger, data
import ctypes, string
import os, shutil
from pathlib import Path
from .mod import Mod
from typing import Generator, Any

from ..typing import LC

def walk(parent:str, exclude:set[str]) -> Generator[tuple[Path,int,int], Any, int]:
    skipped = 0
    total = 0
    if os.path.isfile(parent):
        yield (Path(parent),total,skipped)
    else:
        try:
            for path in os.listdir(parent):
                total += 1
                if path in exclude:
                    skipped += 1
                    continue
                elif path.startswith("$"):
                    skipped += 1
                    continue
                elif "cache" in path:
                    skipped += 1
                    continue
                elif path.startswith("."):
                    skipped += 1
                    continue
                elif path.startswith("Windows"):
                    skipped += 1
                    continue
                elif os.path.exists(parent + "\\" + path):
                    yield (Path(parent + "\\" + path),total,skipped)
                    t = s = 0
                    for p,t,s in walk(parent + "\\" + path, exclude):
                        yield (p, t+total, s+skipped)
                    total += t
                    skipped += s
                    
        except: pass
    return skipped
        

class GameManager:
    def __init__(self) -> None:
        self.game_found = False
        self.mods: dict[str, Mod] = {}
    
    def search_drive(self, d:str, lc:LC):
        folders_searched = 0

        c = 0
        n = 2*32

        exclude = {"Common Files", "Python", "Videos", "Music", "Pictures", "CapCut", "aseprite", "Blender", 
                         "Epic Games", "FL Studio 11", "Git", "Krita (x86)", "Godot", "CapCut Drafts",
                         "ELEGOO SatelLite", "Eclipse Adoptium", "obs-studio", "Java", "JetBrains"}
        for path,total,skipped in walk(d, exclude):
            #print(path)
            c += 1
            if c == n:
                lc.set_statuses(f"Drive {d[0:-1]}, Folders Searched: {folders_searched}/{total}, Folders Skipped {skipped}/{total}", data.game_folder != "", data.steam_folder != "")
                c = 0

            folders_searched += 1

            if path.name == "EscapeTheBackrooms":
                if data.game_folder != "":continue
                if (path / "EscapeTheBackrooms").exists():
                    data.found = True
                    data.game_folder = str(path)
                    print(data.game_folder)
            elif path.name == "Steam":
                if data.steam_folder != "":continue
                if (path / "steam.exe").exists():
                    data.found = True
                    data.steam_folder = str(path)
                    print(data.steam_folder)
            if data.game_folder != "" and data.steam_folder != "": break

    def _find_game(self, lc:LC):
        logger.info("Finding Game and Steam")
        if data.found:
            logger.info("Game already found")
            logger.info("Checking folder")
            if os.path.exists(data.game_folder):
                self.folder = data.game_folder
                return
            logger.info("Folder is wrong")
        for drive in os.listdrives():
            self.search_drive(drive[0:2], lc)
        if not data.found:
            logger.error("Huh? Could not find game.")
        else:
            logger.info("Game Folder Found!")
    
    def find_game(self, lc:LC):
        import threading
        threading.Thread(target=lambda:self._find_game(lc), daemon=False).start()

    def start_game(self):
        import subprocess
        subprocess.call([data.steam_folder+"/steam.exe", "-applaunch", "1943950"])

    def find_mods(self):
        logger.info("Finding Mods")
        self.mods.clear()
        for f in (Path(data.game_folder) / data.mod_path).iterdir():
            mod = Mod(f)
            if mod.name in self.mods: continue
            self.mods.update({mod.name:mod})
            logger.info(f"Found mod {mod}")
        return self.mods
    
    def import_mod(self, import_from:str):
        name = Path(import_from).parts[-1]
        if name in self.mods:
            mod = self.mods[name]
            os.remove(mod.path+(".pak" if mod.enabled else ".dis"))
        shutil.move(import_from, data.game_folder+"/"+data.mod_path+"/"+name)