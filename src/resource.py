
import json

def open_json(path:str):
    j = json.load(open(f"resources/{path}.json", "r", encoding="utf-8"))
    if not isinstance(j, dict):
        raise Exception(f"Invalid json file")
    return j

