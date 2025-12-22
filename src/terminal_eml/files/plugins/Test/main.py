from .plugin_essentials import Plugin

class TestPlugin(Plugin):
    def __init__(self, main, plugins: list) -> None:
        super().__init__(
            main=main, 
            plugins=plugins, 
            display_name="TestMod", 
            id="test_mod"
            )
    
    def initialize(self, *args, **kwargs):
        print("!test")
        return self