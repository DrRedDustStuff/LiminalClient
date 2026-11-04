from tkinter import (
    Toplevel,
    Text,
    Entry,
    Event,
)
from typing import Callable
from blublib.log import Logger

CMD = Callable[[list[str]], int]


class ctx:
    is_open: bool = False

    root: Toplevel
    text: Text
    entry: Entry

    variables: dict[str, int] = {}
    commands: dict[str, CMD] = {}

    queued_text: list[str] = []


def reg(fnc: CMD):
    ctx.commands.update({fnc.__name__: fnc})
    return fnc


def queued_text(text: str):
    ctx.queued_text.append(text)


def unstring(args: list[str]) -> list[str]:
    result = []
    for arg in args:
        if arg.startswith('"'):
            result.append(arg[1:-1])
            continue
        result.append(arg)
    return result


def get_kwargs(args: list[str]) -> dict[str, str]:
    result = {}

    for arg in args:
        v = arg.split("=")
        if len(v) != 2:
            continue

        result.update({v[0]: v[1]})

    return result


Logger.add_handle(queued_text)


def append_text(*txt: str, sep: str = " ", end: str = "\n"):
    ctx.text.configure(state="normal")
    ctx.text.insert("insert", sep.join(txt) + end)
    ctx.text.configure(state="disabled")


def execute_command(text: str):
    v = text.split(" ", 1)
    c = v[0]
    if c in ctx.commands.keys():
        # Execute command
        fnc = ctx.commands[c]
        if len(v) == 1:
            code = fnc([])  # pyright: ignore[reportCallIssue]

        else:
            args = []
            t = 0
            collected = ""
            for c in v[1].strip():
                if c == '"':
                    if t == 0:
                        t = 1
                    elif t == 1:
                        t = 0
                        args.append(collected)
                        collected = ""
                        
                elif t == 1:
                    collected += c


                elif c == " ":
                    args.append(collected)
                    collected = ""
                    continue

                elif t == 0:
                    collected += c

            args.append(collected)

            # args = v[1].strip().split(" ")
            while "" in args:
                args.remove("")

            code = fnc(unstring(args))  # pyright: ignore[reportCallIssue]

        if code != 0:
            append_text("Non 0 exit code", str(code), ".")

    else:
        append_text("Command", c, "is not a command.")

def enter(ev: Event):
    if ev.keycode != 13:
        return

    text = ctx.entry.get()
    ctx.entry.delete(0, "end")

    append_text("> " + text)
    execute_command(text)


def initialize():
    if ctx.is_open:
        return
    ctx.is_open = True

    ctx.root = Toplevel()
    ctx.root.title("Console")
    ctx.root.geometry("800x650")

    ctx.entry = Entry(ctx.root, font=("TkTextFont", 12))
    ctx.entry.pack(side="bottom", fill="x", padx=1, pady=1)

    ctx.text = Text(ctx.root, state="disabled", wrap="none")
    ctx.text.pack(fill="both", expand=True, padx=1, pady=1)

    ctx.entry.bind("<KeyPress>", enter)

    for text in ctx.queued_text:
        append_text(text)

    Logger.add_handle(lambda text: append_text(text))
