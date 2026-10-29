from src import console
from src import main
from src import data
from blublib import resource
import sys
import os.path

def init() -> None:
    ...

    
@console.reg
def force_quit(_):
    "force_quit | Force quits Liminal client"
    sys.exit()

@console.reg
def echo(args: list[str]):
    "echo <*text> | Prints text to the console"
    console.append_text(" ".join(args))
    return 0

@console.reg
def restart(_):
    "restart | Restarts Liminal client, this may come with bugs"
    console.append_text("Be aware that restarting can cause some problems")
    main.get_instance().stop()
    main.get_instance().start()
    return 0

@console.reg
def data_var(args: list[str]):
    "data_var <name> | displays value of the variable inside data"
    varname = args[0]

    if not hasattr(data, varname):
        console.append_text("No variable named",varname,"in data")
        return 1
    
    console.append_text("Value: ", str(getattr(data, varname)))

    return 0

@console.reg
def exec(args: list[str]):
    "exec <plugin> <file> | Executes file inside plugin data/scripts folder"
    if len(args) != 2:
        console.append_text("Missing arguments")
        return 1
    plugin = args[0]
    file = args[1]
    path = resource.data(plugin, os.path.join("scripts",file))

    if not path.endswith(".src"):
        path += ".src"
    if not os.path.exists(path):
        console.append_text("File", path, "Does not exist")

    with open(path, "r") as ref:
        for line in ref.read().split("\n"):
            line = line.split("//")[0].strip()
            if line == "": continue

            console.execute_command(line)

        ref.close()

    return 0

@console.reg
def help(args: list[str]):
    "help <command> | Show help for the command"
    if len(args) == 0:
        for k,cmd in console.ctx.commands.items():
            console.append_text(cmd.__doc__ if cmd.__doc__ else "No documentation")
        return 0

    cmd = args[0]
    if not cmd in console.ctx.commands.keys():
        console.append_text("Command",cmd,"is not in commands list")
        return 1

    command = console.ctx.commands[cmd]
    console.append_text(command.__doc__ if command.__doc__ else "No documentation")
    return 0