from customtkinter import CTkImage, CTkFont
from PIL import Image
import os

# if not os.path.exists("./src/resources/"):
#     raise Exception("Please add a resources folder with: font (optional), image (required), lang (optional), sound (optional), theme (required)")

class Identifier:
    _namespace:str
    _path:str
    @classmethod
    def get(cls,namespace:str,path:str):
        self = cls()
        self._namespace = namespace
        self._path = path
        return self

    def getNamespace(self):
        return self._namespace
    
    def getPath(self):
        return self._path

    def pathSuffix(self,suffix:str):
        new = Identifier()
        new._namespace = self._namespace
        new._path = self._path + "." + suffix
        return new

    def pathPrefix(self,prefix:str):
        new = Identifier()
        new._namespace = self._namespace
        new._path = prefix + "." + self._path
        return new

    @classmethod
    def id(cls,path:str):
        return cls.get("liminal_client",path)

    def __repr__(self) -> str:
        return "<Identifier namespace:%s path:%s hash:%s>" % (self._namespace,self._path,self.__hash__())

    def __hash__(self) -> int:
        return (self._namespace + "." + self._path).__hash__()

    # # Fixes
    # def ljust(self, width, fillchar = " "):
    #     return self.__repr__()

_appdata = "C:/Users/%s/AppData/Local/%s/" % (os.getlogin(),"LiminalClient")

import os
import os.path
import shutil


def path(plugin: str, p: str):
    return "./" + os.path.join("plugins", plugin, "resources", p)

def data(plugin: str, p: str):
    return "./" + os.path.join("plugins", plugin, "data", p)

_image_cache: dict[str, CTkImage] = {}
# Source

def image(plugin: str, p: str, size: tuple[int, int] = (20, 20), use_variations: bool = False):
    f = path(plugin, "image/" + p)
    if use_variations:
        raise Exception("Not implemented")
    else:
        image = Image.open(f)
        if not p in _image_cache.keys():
            _image_cache.update({p: CTkImage(image, image, size)})
        return _image_cache[p]


def datapath(p: str):
    return _appdata + p.removeprefix("/").removeprefix("./")


def font(
    family: str | None,
    size: int,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    overstrike: bool = False,
):
    return CTkFont(
        family,
        size,
        "bold" if bold else "normal",
        "italic" if italic else "roman",
        underline,
        overstrike,
    )


def load() -> None:
    ...