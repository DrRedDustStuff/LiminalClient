import json
import os, shutil
from . import data

def get_path(path:str):
    return data.app_data + "LiminalClient/resources/" + path
    

def open_json(path:str):
    j = json.load(open(f"./resources/{path}.json", "r", encoding="utf-8"))
    if not isinstance(j, dict):
        raise Exception(f"Invalid json file")
    return j


def move_to_appdata():
    data.built = not os.path.exists("./not_built")
    
    d = "x"
    if os.path.exists("./resources/"):
        if os.path.exists(data.app_data+"LiminalClient/"):
            if os.path.exists(data.app_data+"LiminalClient/resources/data"):
                with open(data.app_data+"LiminalClient/resources/data", "r", encoding="utf-8") as r:
                    d = r.read()
                    r.close()
            shutil.rmtree(data.app_data+"LiminalClient/resources/")
        if os.path.exists("./not_built"):
            shutil.copytree("./resources/", data.app_data+"LiminalClient/resources/")
            with open(data.app_data+"LiminalClient/resources/data", "w", encoding="utf-8") as w:
                w.write(d)
                w.close()
        else:
            shutil.move("./resources/", data.app_data+"LiminalClient/resources/")
        
    os.chdir(data.app_data+"LiminalClient/")

