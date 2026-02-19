from .. import logger, data
import ctypes, string
import os, shutil
from pathlib import Path
from .mod import Mod

class GameManager:
    def __init__(self) -> None:
        self.game_found = False
        self.mods: dict[str, Mod] = {}
    
    def search_drive(self, d:str):
        folders_searched = 0
        folders_skipped = 0
        total_folders = 0
        for path, dirnames, filenames in Path(d).walk():
            print(f"Drive {d[0:-1]}, Folders Searched: {folders_searched}/{total_folders}, Folders Skipped {folders_skipped}/{total_folders}                    \r", end="")

            total_folders += 1

            l = False
            for i in path.parts:
                if "cache" in i: l = True
                elif i in {"Common Files", "Python", "Videos", "Music", "Pictures", "CapCut", "aseprite", "Blender", 
                         "Epic Games", "FL Studio 11", "Git", "Krita (x86)", "Godot", "CapCut Drafts",
                         "ELEGOO SatelLite", "Eclipse Adoptium", "obs-studio", "Java", "JetBrains"}: l = True
                elif i.startswith("."): l = True
                elif i.startswith("Windows"): l = True
                if l: break
            if l or not path.is_dir():
                folders_skipped += 1
                continue

            folders_searched += 1

            if path.name == "EscapeTheBackrooms":
                if data.game_folder != "":continue
                if (path / "EscapeTheBackrooms").exists():
                    data.found = True
                    data.game_folder = str(path)
            elif path.name == "Steam":
                if data.steam_folder != "":continue
                if (path / "steam.exe").exists():
                    data.found = True
                    data.steam_folder = str(path)
            if data.game_folder != "" and data.steam_folder != "": break

        print()

    def _find_game(self):
        logger.info("Finding Game and Steam")
        if data.found:
            logger.info("Game already found")
            logger.info("Checking folder")
            if os.path.exists(data.game_folder):
                self.folder = data.game_folder
                return
            logger.info("Folder is wrong")
        for drive in os.listdrives():
            self.search_drive(drive)
        if not data.found:
            logger.error("Huh? Could not find game.")
        else:
            logger.info("Game Folder Found!")
    
    def find_game(self):
        import threading
        threading.Thread(target=self._find_game, daemon=False).start()

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