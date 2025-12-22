from typing import Self, Any, Callable
from .commands import Command
from .commands import *

def command(name:str, function, takes_arguments:bool=False, help_file:str="nohelp.txt") -> dict[str, dict[str, Any]]:
    """
    :param name: this is the lowercase name of the function (used in finding the command you typed, due to consistency this should always be invisible)
    :param function: the function to call, must take one argument of type `Command` if `takes_arguments` is `True` else it should not take any positional arguments
    :param takes_arguments: controls whether the command handler gives arguments (`Command` Object) to this function or not
    :param help_file: the file to use when help `[this command]` is used, should contain a good enough explanation of how this command works and how to use it
    """
    return { name: {
        "func":      function,
        "args":      takes_arguments,
        "help_file": help_file
    } }

class TerminalEML:
    @classmethod
    def new(cls) -> Self:
        return cls()

    def __init__(self) -> None:
        self.running = True

        from .game_manager.folder_handler import FolderHandler
        from .game_manager.game import EscapeTheBackrooms
        from .mod import Mod, ModKeeper
        self.files_folder = FolderHandler(folder_path="./files/mods")
        self.escape_the_backrooms_folder = EscapeTheBackrooms("")
        self.mod_keeper = ModKeeper("")

        self.commands: dict[str, dict[str, Any]] = {}
    
    def update_command(self, name:str, function, takes_arguments:bool=False, help_file:str="nohelp.txt") -> None:
        cmd: dict[str, dict[str, Any]] = command(
            name=name,
            function=function,
            takes_arguments=takes_arguments,
            help_file=help_file
            ) 
        self.commands.update(cmd)

    @classmethod
    def start(cls) -> Self:
        new: Self = cls.new()
        new.load()
        new.run()
        return new
    

    def execute_command(self, command:list[str]) -> None:
        if not command[0] in self.commands: return # ignore non existent commands
        command_data = Command(command=command)

        found_command: dict[str, Any] = self.commands[command_data.command]
        if found_command["args"]: found_command["func"](self, command_data)
        else:                     found_command["func"](self)

    def load(self) -> None:
        self.load_commands()
        self.load_plugins()
        self.load_cache()
        cget_mods(self)
        return

    def load_cache(self):
        from pathlib import Path
        f: str = ""
        with open("./files/game_folder.cache", "r") as c:
            for folder in c.readlines():
                if Path(folder).exists():
                    f = folder
                    break
            if f == "":
                print("Please re find the game folder. (Use: fgame)")
        self.escape_the_backrooms_folder.reselect_folder(f)
        self.mod_keeper.set_folder(self.escape_the_backrooms_folder.folder)

    def load_commands(self):
        self.update_command(name="exit",    function=cexit,                    takes_arguments=False, help_file="exit.txt")
        self.update_command(name="brexit",  function=cbrexit,                  takes_arguments=False, help_file="exit.txt")
        self.update_command(name="help",    function=chelp,                    takes_arguments=True,  help_file="help.txt")

        self.update_command(name="clear",   function=cclear,                   takes_arguments=True,  help_file="clear.txt")
        self.update_command(name="clean",   function=cclean_game_folder_cache, takes_arguments=False, help_file="clean.txt")

        self.update_command(name="fgame",   function=cfind_game,               takes_arguments=False, help_file="nohelp.txt")
        self.update_command(name="start",   function=cstart_game,              takes_arguments=False, help_file="nohelp.txt")

        self.update_command(name="menable", function=cmod_enabled,             takes_arguments=True,  help_file="nohelp.txt")
        self.update_command(name="lsmods",  function=clist_mods,               takes_arguments=False, help_file="nohelp.txt")
        self.update_command(name="umods",   function=cset_mods,                takes_arguments=False, help_file="nohelp.txt")

        self.update_command(name="test",    function=ctest,                    takes_arguments=False, help_file="nohelp.txt")

    def load_plugins(self) -> None:
        from .plugin import Plugin
        from .plugin import ModuleType, load_plugins

        plgs: list[tuple[ModuleType, Any]] = load_plugins(plugins_directory="files/plugins")
        self.plugins: list[tuple[ModuleType, Plugin, Any]] = []
        for plugin in plgs:
            self.plugins.append((plugin[0], plugin[0].Plugin(self, plgs).initialize(), plugin[1]))

    def run(self) -> None:
        while self.running:
            self.cycle()
    
    def cycle(self) -> None:
        inp: str = input(">>")
        self.execute_command(command=inp.split(sep=" "))