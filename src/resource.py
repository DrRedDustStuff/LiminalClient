import json
import os, shutil
from . import data

def get_path(path:str):
    #C:\Users\mrbui\AppData\Local\LiminalClient\resources
    return data.app_data + "LiminalClient/resources/" + path
    

def open_json(path:str):
    j = json.load(open(f"./resources/{path}.json", "r", encoding="utf-8"))
    if not isinstance(j, dict):
        raise Exception(f"Invalid json file")
    return j


def move_to_appdata():
    if os.path.exists("./not_built"):
        if os.path.exists(data.app_data+"LiminalClient/"): shutil.rmtree(data.app_data+"LiminalClient/resources/")
        shutil.copytree("./resources/", data.app_data+"LiminalClient/resources/")
        data.built = True

    elif os.path.exists("./resources/"):
        shutil.move("./resources/", data.app_data+"LiminalClient/resources/")

    os.chdir(data.app_data+"LiminalClient/")

