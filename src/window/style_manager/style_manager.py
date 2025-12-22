import platform, json

from typing import Any
from .tkstyle_reader import TKStyle

OSTRANSLATION: dict[str, str] = {
    "Linux":"Linux",
    "Darwin":"Mac",
    "Windows":"Windows"
}

def os_name():
    return OSTRANSLATION.get(platform.platform(), "Windows")

# TODO:
# - load styles depending on system
# - return font data on __call__ function

class StyleManager:
    def __init__(self,style_directory: str) -> None:
        os: str = OSTRANSLATION.get(platform.platform(), "Windows") # get os name, default to windows if its not found (unlikely)
        self.style: dict[str, dict[str, str | int]] = json.load(open(f"{style_directory}/{os}.json", "r"))

    def get_item_by_path(self, jsn:dict[str, Any], path:str):
        new_path = path.split(".")
        result: dict[str, Any] | Any = jsn
        #print(f"{new_path}\n{jsn}")
        for name in new_path:
            result = result.get(name, "NotFound")
        return result

    def __call__(self, type_path:str) -> tuple[str, int, str]:
        return tuple(i[1] for i in self.get_item_by_path(self.style, type_path).items())