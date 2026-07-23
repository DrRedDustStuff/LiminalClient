from pygame import mixer
from . import resource
mixer.init()

def load(id:str,type:str="mp3"):
    return mixer.Sound(resource.path("sound/"+id+"."+type))

# == Sounds == #
swoosh = load("swoosh","wav")

# == Channels == #
notification_channel = mixer.Channel(0)
notification_channel.set_volume(0.05)
def notification(sound:mixer.Sound):
    notification_channel.play(sound,fade_ms=500)
