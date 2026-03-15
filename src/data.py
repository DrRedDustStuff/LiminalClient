import os
from . import logger

major = 0
minor = 2
build = 6
revision = 0
type = "beta"

version = f"{major}.{minor}{"-"+type if type != "" else ""}"

built = False

# Helper
mod_path = r"EscapeTheBackrooms/Content/Paks/--ModLoader--"
movie_path = r"EscapeTheBackrooms/Content/Movies"

app_data = fr"C:/Users/{os.getlogin()}/AppData/Local/"
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

def load():
    logger.info("Loading data")
    global first_time
    if not os.path.exists("./resources/data"):
        open("./resources/data", "x", encoding="utf-8").write("x")
        first_time = True
        return
    
    global found
    global game_folder
    global steam_folder
    
    f = open("./resources/data", "r", encoding="utf-8")
    d = f.read().split("\n")
    if len(d) == 1:
        logger.info("Data file is empty, Using default values")
        first_time = True
        return
    found = d[0] == "t"
    game_folder = d[1]
    steam_folder = d[2]

def save():
    logger.info("Saving data")
    f = open("./resources/data", "w", encoding="utf-8")

    global found
    global game_folder

    d = [
        "t" if found else "f",
        game_folder,
        steam_folder,
        version
    ]

    f.write("\n".join(d))