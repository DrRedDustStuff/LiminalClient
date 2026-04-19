import os, sys
from . import logger
from tkinter import messagebox

major = 0
minor = 4
build = 1
revision = 0
type = "beta"

version = f"{major}.{minor}{"-"+type if type != "" else ""}"

built = False

# Helper
mod_path = "EscapeTheBackrooms/Content/Paks/--ModLoader--"
movie_path = "EscapeTheBackrooms/Content/Movies"

app_data = f"C:/Users/{os.getlogin()}/AppData/Local/"
etb_config = app_data+"EscapeTheBackrooms/Saved/Config/WindowsNoEditor/"

etb_user_settings = etb_config+"GameUserSettings.ini"
etb_input = etb_config+"Input.ini"

size = (850,550)
window_pos = (0,0)

# Data default state
first_time = False
found = False
game_folder = ""
steam_folder = ""
theme = "_Blue"

def load():
    logger.info("Loading data")
    global first_time
    if not os.path.exists(app_data + "LiminalClient/resources/data"):
        open(app_data + "LiminalClient/resources/data", "x", encoding="utf-8").write("x")
        first_time = True
        return
    
    global found
    global game_folder
    global steam_folder
    global theme
    
    f = open(app_data + "LiminalClient/resources/data", "r", encoding="utf-8")
    d = f.read().split("\n")
    if len(d) == 1:
        logger.info("Data file is empty, Using default values")
        first_time = True
        return
    found = d[0] == "t"
    game_folder = d[1]
    steam_folder = d[2]
    theme = d[4]

def save():
    logger.info("Saving data")
    try:
        f = open(app_data + "LiminalClient/resources/data", "w", encoding="utf-8")
    except PermissionError as perm_error:
        messagebox.showerror("Could not open file", f"""Error:{perm_error}
could not open data file. this will hopefully get fixed soon,
until then run Liminal Client as administrator.""")
        sys.exit(1)

    d = [
        "t" if found else "f",
        game_folder,
        steam_folder,
        version,
        theme
    ]
    print(d)

    f.write("\n".join(d))