from typing import Callable

class Plugin:
    def __init__(self, main, plugins:list, display_name:str, id:str) -> None:
        self.main = main
        self.plugins = plugins
        self.display_name = display_name
        self.id = id.lower()
    
    def initialize(self, *args, **kwargs):
        return self

## Typing ##
class Command:
    def __init__(self, command:list[str]) -> None:
        self.command: str = command[0]
        self.flags: list[str] = []
        self.args: list[str] = []
        self.kwargs: list[tuple[str, str]] = []
        self.argc = 0
        self.kwargc = 0

## Rename ##
def reg_cmd(main, name:str, function:Callable, takes_arguments:bool=False, help_file:str="nohelp.txt"):
    """
    :param main: this is the main class (you can use self.main as the parameter name)
    :param name: this is the lowercase name of the function (used in finding the command you typed, due to consistency this should always be invisible)
    :param function: the function to call, must take one argument of type `Command` if `takes_arguments` is `True` else it should not take any positional arguments
    :param takes_arguments: controls whether the command handler gives arguments (`Command` Object) to this function or not
    :param help_file: the file to use when help `[this command]` is used, should contain a good enough explanation of how this command works and how to use it
    """
    main.update_command(name, function, takes_arguments, help_file)

def reg_help_file(main, mod_name:str, name:str, file:str) -> None:
    # POV:
    # unhinged code fr
    with open(file=f"files/help_files/{name}", mode="w") as f:
        with open(file=f"files/plugins/{mod_name}/{file}", mode="r") as g:
            print(f"files/plugins/{mod_name}/{file}")
            f.write(g.read())