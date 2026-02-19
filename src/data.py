import os
from . import logger

major = 0
minor = 1
small = 0
type = "beta"

version = f"{major}.{minor}.{small}{"-"+type if type != "" else ""}"

# Helper
mod_path = r"EscapeTheBackrooms/Content/Paks/--ModLoader--"
movie_path = r"EscapeTheBackrooms/Content/Movies"

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
        steam_folder
    ]

    f.write("\n".join(d))