from string import ascii_uppercase
from os import path, walk
from pathlib import Path
from threading import Thread

from .folder_handler import FolderHandler, cache

class EscapeTheBackrooms(FolderHandler):
    def __init__(self, folder_path: str) -> None:
        super().__init__(folder_path)
    
    def find_game_folder(self):
        with open(f"./files/game_folder.cache", "r") as c:
            for folder in c.readlines():
                if not Path(folder).exists(): continue
                print()
                self.reselect_folder(folder)
                return -1

        for drive in self.get_all_drives():
            folder = self.deep_search(
                from_folder=drive,
                to_folder="EscapeTheBackrooms",
                checkpoints={"steamapps"},
                exclude={"AppData", "Windows", "$RECYCLE.BIN", "Epic Games", "Microsoft Visual Studio", "UnityEditor", "Users"},
                depth=32)
            if folder:
                cache(folder, "./files/game_folder")
                self.reselect_folder(folder)
                return 0

    def deep_search(self, from_folder: str, to_folder: str, checkpoints: set[str], exclude: set[str], depth: int) -> str | None:
        from os import walk, path, sep
        looked_at = 0
        
        for root, dirs, _ in walk(from_folder):
            looked_at += 1
            parts = root.split(sep)   # do this once, reuse later

            # 🔹 Skip if any excluded folder is in path
            if any(p in exclude for p in parts):
                continue

            # 🔹 Check if target folder is in this directory
            if to_folder in dirs:
                # Ensure at least one checkpoint exists in path
                if checkpoints & set(parts):
                    return path.join(root, to_folder)

            # 🔹 Depth limit
            if len(parts) > depth:
                # Modify dirs in-place to stop walk() from going deeper
                dirs[:] = []
                continue

            print(f"\rlooked at {looked_at} folders in {from_folder}", end="")
        
        print("")  # newline after progress
        return None

    def get_all_drives(self):
        # Helper function
        drives = []
        for l in ascii_uppercase:
            d = f"{l}:/"
            if path.exists(d):
                drives.append(d)
        
        return drives
