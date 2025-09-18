import ctypes, string, subprocess, os, requests
from pathlib import Path

# i dont understand this code tbh
def get_logical_drives():
    drives = []
    bitmask = ctypes.cdll.kernel32.GetLogicalDrives()
    for letter in string.ascii_uppercase:
        if bitmask & 1:
            drives.append(f"{letter}:\\")
        bitmask >>= 1
    return drives


# i made this tho (so i understand it)
class Game:
    """
    #### Container class for found games and their ids/folders
    """
    def __init__(self) -> None:
        pass

class Steam:
    """
    ## Steam API accessing class
    <b>can access: </b>
    - steam games
    - game folders
    - game id's
    - can run steam games by id
    """
    def __init__(self) -> None:
        ...
        ## TODO 
        # add game folder finding -easy
        #
    def find_steam(self):
        likely_folders = [
            "Program Files (x86)",
            "Program Files",
            os.path.join("Users", os.getlogin(), "AppData", "Local"),
            os.path.join("Users", os.getlogin(), "AppData", "Roaming"),
        ]

        drives = get_logical_drives()
        for drive in drives:
            for folder in likely_folders:
                path = os.path.join(drive, folder, "Steam", "steam.exe")
                if os.path.isfile(path):
                    print(f"Found Steam: {path}")
                    return path
        return None

    def rgid(self, steam_path:str, game_id:int):
        subprocess.run([steam_path, "-applaunch", f"{game_id}"])

    def gameid(self, name):
        url = "https://store.steampowered.com/api/storesearch/"
        params = {
            "term": name,
            "l": "english",
            "cc": "US"
        }
        response = requests.get(url, params=params)
        data = response.json()
        for item in data.get("items", []):
            if item["name"].lower() == name.lower():
                return item["id"]
        return None