from typing import Self, Any

def command(name:str, function, takes_arguments:bool=False, help_file:str="nohelp.txt"):
    """
    :param function: The function to use (callable) should not take arguments, unless takes_arguments is `True`
    :param takes_arguments: controls whether the command handler gives arguments (`Command` Object) to this function or not
    :param help_file: the file to use if help <Command> is used, it reads the file and prints it as help on how to use the command
    """
    return {name:{
        "func":function,
        "args":takes_arguments,
        "help_file":help_file
    }}

from commands import Command
import commands as cmd

class TerminalEML:
    @classmethod
    def new(cls):
        return cls()

    def __init__(self) -> None:
        self.running = True

        self.commands: dict[str, dict[str, Any]] = { }
        self.commands.update(command("exit", cmd.exit, False, "exit.txt"))
        self.commands.update(command("help", cmd.help, True,  "help.txt"))

    @classmethod
    def start(cls):
        new = cls.new()
        new.load()
        new.run()
        return new
    

    def execute_command(self, command:list[str]):
        if not command[0] in self.commands: return # ignore non existent commands
        command_data = Command(command)

        found_command = self.commands[command_data.command]
        if found_command["args"]: found_command["func"](self, command_data)
        else:                     found_command["func"](self)

    def load(self):
        self.load_plugins()
        return

    def load_plugins(self):
        from plugins import Plugin
        from plugin import ModuleType, load_plugins

        plgs: list[ModuleType] = load_plugins("plugins")
        plugins: list[tuple[ModuleType, Plugin]] = []
        for plugin in plgs:
            plugins.append((plugin, plugin.Plugin(self, plgs).initialize()))


    def run(self):
        while self.running:
            self.cycle()
    
    def cycle(self):
        inp = input(">>")
        self.execute_command(inp.split(" "))

if __name__ == "__main__":
    terminal_eml = TerminalEML.start()