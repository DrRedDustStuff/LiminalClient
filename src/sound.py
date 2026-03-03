from pygame import mixer

mixer.init()

_sounds: dict[str,mixer.Sound] = {}

def loadsound(file:str, id:str):
    _sounds.update({id:mixer.Sound(file)})

def configsound(id:str, volume:float=1,fadeout:int=0):
    s = _sounds[id]
    s.set_volume(volume)
    s.fadeout(fadeout)

def playsound(id:str):
    _sounds[id].play()