from .plugin_essentials import reg_cmd, reg_help_file, Command, Plugin
from typing import Any
from types import ModuleType
import sys

# ill do it later

def list_plugins(self):
    for plgn in self.plugins:
        plugin: Plugin = plgn[1]
        print(f"Name: {plugin.display_name} [{plugin.id}]")

def reload_plugins(self):
    print("[Reloading Plugins]")
    for plugin, _, _ in self.plugins:
        print(plugin.__name__, "\n", plugin)
        sys.modules.pop(plugin.__name__)
    self.plugins = []
    self.load_plugins()

def help_plugin(self, command:Command):
    # help with a plugin, show the help file
    pass

def RegisterCommands(main):
    reg_cmd(main, "plugins",   list_plugins,   False, "plgh.plugin_manager.txt")
    reg_cmd(main, "rlplugins", reload_plugins, False, "nohelp.txt")
    reg_cmd(main, "help-plg",  help_plugin,    False, "nohelp.txt")
    
def RegisterHelpFiles(main, mod_name:str):
    reg_help_file(main, mod_name, "plgh.plugin_manager.txt", "plugin_manager.txt")