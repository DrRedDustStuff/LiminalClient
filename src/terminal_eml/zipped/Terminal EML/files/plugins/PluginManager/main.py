from .plugin_essentials import Plugin

class PluginManagerPlugin(Plugin):
    def __init__(self, main, plugins: list) -> None:
        super().__init__(
            main,
            plugins, 
            "PluginManager", 
            "plugin_manager_plugin"
            )
    
    def initialize(self, *args, **kwargs):
        from .commands import RegisterCommands, RegisterHelpFiles
        RegisterCommands(self.main)
        RegisterHelpFiles(self.main, self.display_name)
        return super().initialize(*args, **kwargs)