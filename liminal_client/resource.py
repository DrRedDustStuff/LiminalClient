from customtkinter import (
    CTkImage
)
from PIL import Image
from . import data

_root = "./resources/"
_appdata = "C:/Users/%s/AppData/Local/LiminalClient"%data.login

def path(p:str):
    return _root + p.removeprefix("/").removeprefix("./")

def image(p:str,size:tuple[int,int]=(20,20),use_variations:bool=False):
    f = path("image/"+p)
    if use_variations:
        raise Exception("Not implemented")
    else:
        image = Image.open(f)
        return CTkImage(image,image, size)


def datapath(p:str):
    return _appdata + p.removeprefix("/").removeprefix("./")

