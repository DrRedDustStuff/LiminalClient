class Command:
    def __init__(self, command:list[str]) -> None:
        self.command: str = command[0]
        self.flags: list[str] = []
        self.args: list[str] = []
        self.kwargs: list[tuple[str, str]] = []

        for operand in command[1:]:
            if    operand.startswith("--"): self.flags.append(operand[2:])
            elif  "=" in operand:
                kwarg = operand.split("=", 1)
                self.kwargs.append((kwarg[0], kwarg[1]))
            else:                                  self.args.append(operand)

        self.argc = len(self.args)
        self.kwargc = len(self.kwargs)

def cexit(self):
    self.running = False

def cbrexit(self):
    from time import sleep
    print("the united kingdom decides to leave the UE")
    sleep(0.3)
    print("they realize it was'nt the best idea")
    sleep(0.4)
    exit(self)

def chelp(self, command:Command):
    if command.argc == 0:
        with open(
            "files/help_files/help_noargs.txt",
            "r"
        ) as f:
            print(f.read())
    else:
        with open(
            f"files/help_files/{self.commands[ command.args[0] ][ "help_file" ]}",
            "r"
        ) as f:
            print(f.read())

def cfind_game(self):
    from time import time
    stt = time()
    code = self.escape_the_backrooms_folder.find_game_folder()
    if code == 0: print(f"\nFound Game folder at {self.escape_the_backrooms_folder.folder}")
    elif code == -1: print(f"Used cached Game folder {self.escape_the_backrooms_folder.folder}")
    print(f"Took {(time() - stt):.2f} seconds")

def cmod_enabled(self, command:Command):
    # disable/enable (arg1) the selected mod (arg0)
    if command.argc < 2:
        print("please provide more arguments")
        return
    mod: str = command.args[0]
    state = True if (command.args[1] == "Enabled") else (False if (command.args[1] == "Disabled") else None)
    if state is None:
        print("state is invalid")
        return
    from pathlib import Path
    file = self.mod_keeper[mod].file
    if not Path(file):
        print("[Internal] Mod file not found")
        return
    self.mod_keeper[mod].state = state
    print(f"Mod state updated to {self.mod_keeper[mod].state}")

def cclear(self, command:Command):
    # Clear something.
    # e.g.: game_folder
    if command.argc == 0:
        print("Please provide a cache to delete. Use 'help clear' to see the list of caches")
        return
    match command.args[0]:
        case "game_folder":
            with open("./files/game_folder.cache", "w") as c:
                c.write("") # clear the game folder cache
            print("cleared the game folder cache")

from pathlib import Path
def cclean_game_folder_cache(self):
    f:str = ""
    with open("./files/game_folder.cache", "r") as c:
        for folder in c.readlines():
            if Path(folder).exists(): f = folder
    with open("./files/game_folder.cache", "w") as c:
        c.write(f)
    print("Successfully cleaned the Game folder cache")

def cget_mods(self):
    from .mod import Mod
    from os import listdir
    for file in listdir(f"{self.escape_the_backrooms_folder.folder}/EscapeTheBackrooms/Content/Paks/--ModLoader--"):
        mod: list[str] = file.split(".")
        name: str = mod[0]
        disabled: bool = len(mod) == 3 and mod[2] == "dis"
        #print(f"mod: {name}, {"Enabled" if not disabled else "Disabled"}")
        self.mod_keeper.append(Mod(name,file,not disabled))

def cset_mods(self):
    from .mod import Mod
    from os import listdir, rename, path
    folder = f"{self.escape_the_backrooms_folder.folder}/EscapeTheBackrooms/Content/Paks/--ModLoader--"
    for file in listdir(folder):
        mod: list[str] = file.split(".")
        name = mod[0]
        _mod = self.mod_keeper[mod[0]]
        print(f"updating mod {name} to state {_mod.state}")
        rename(path.join(folder, file), path.join(folder, f"{name}.{"pak" if _mod.state else "pak.dis"}"))

def clist_mods(self):
    from .mod import Mod

    mod:Mod = Mod("","",False)
    for mod in self.mod_keeper.__mods__:
        print(f"mod: {mod.name}, {"Enabled" if mod.state else "Disabled"}")

def cstart_game(self):
    import subprocess
    subprocess.run(["start", f"steam://rungameid/1943950"], shell=True)

def ctest(self):
    from os import sep
    print("\n\r")
    print(r"D:/root\thing\dude\haha".split(sep))