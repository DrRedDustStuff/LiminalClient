from pygame import mixer
import os.path
from . import resource
mixer.init()

from pygame.mixer import Channel, Sound

def load(plugin: str,id:str,type:str="mp3"):
    return mixer.Sound(resource.path(plugin, os.path.join("sound",id+"."+type)))
