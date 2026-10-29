
from blublib import sound

# == Sounds == #
swoosh = sound.load("Source", "swoosh","wav")

# == Channels == #
notification_channel = sound.Channel(0)
notification_channel.set_volume(0.5)
def notification(sound:sound.Sound):
    notification_channel.play(sound,fade_ms=500)
