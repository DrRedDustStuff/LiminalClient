from blublib.plugin.plugin import Plugin

class SourceInit(Plugin):
    def __init__(self) -> None:
        super().__init__()
        from . import console_commands
        console_commands.init()

    def initialize(self): ...
    def load(self): ...
    def unload(self): ...