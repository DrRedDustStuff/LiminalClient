class Plugin:
    id: str = ""
    version: str = "1.0"

    def __init__(self) -> None: pass
    "Called when the plugin is discovered"

    def load(self): print("Plugin %s does not have a load function"%(type(self).__name__))
    "Called when plugin is loaded\nFunction for binding events or loading files"
    def initialize(self):  print("Plugin %s does not have a initialize function"%(type(self).__name__))
    "Called when plugin is initialized (after all liminal client stuff is loaded)"
    def unload(self):  print("Plugin %s does not have a unload function"%(type(self).__name__))
    "Called when plugin is unloaded (after liminal client stops)\nFunction for unloading files"

    def represent(self) -> str: return type(self).__name__
    def __repr__(self) -> str: return self.represent()