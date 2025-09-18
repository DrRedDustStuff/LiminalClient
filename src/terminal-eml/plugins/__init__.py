

class Plugin:
    def __init__(self, main, plugins:list, display_name:str, id:str) -> None:
        self.main = main
        self.plugins = plugins
        self.display_name = display_name
        self.id = id.lower()
    
    # main initialization function (should return nothing)
    def initialize(self, *args, **kwargs):...