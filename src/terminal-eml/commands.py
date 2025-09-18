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

def exit(self):
    self.running = False

def help(self, command:Command):
    if command.argc == 0:
        with open(
            "help_files/help_noargs.txt",
            "r"
        ) as f:
            print(f.read())
    else:
        with open(
            f"help_files/{self.commands[command.command]["help_file"]}",
            "r"
        ) as f:
            print(f.read())