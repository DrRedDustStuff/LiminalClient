from typing import Any

colors = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
    "none": "none",
}
backgrounds = {
    "black": "40",
    "red": "41",
    "green": "42",
    "yellow": "43",
    "blue": "44",
    "magenta": "45",
    "cyan": "46",
    "white": "47",
    "none": "none",
}
bolds = {True: "1", False: "none"}
darkens = {True: "2", False: "none"}
underlines = {True: "4", False: "none"}


def evaluate(msg: dict[str, Any]) -> str:
    color = msg.get("color", "none")
    background = msg.get("background", "none")
    bold = msg.get("bold", False)
    underline = msg.get("underline", False)
    darken = msg.get("darken", False)
    if msg.get("header", False):
        color = "magenta"
        background = "none"
        bold = True
        darken = False

    c = colors[color]
    bg = backgrounds[background]
    b = bolds[bold]
    u = underlines[underline]
    d = darkens[darken]

    text = msg.get("text", "")
    if isinstance(text, list):
        text = " ".join(text)
    elif isinstance(text, tuple):
        text = " ".join(text)
    text = str(text)

    l = [c, bg, b, u, d]
    while "none" in l:
        l.remove("none")

    return "\033[" + ";".join(l) + "m" + text + "\033[0m"


def text(msg: dict[str, Any] | list[dict[str, Any]]):
    if isinstance(msg, dict):
        return evaluate(msg)
    else:
        t = ""
        for m in msg:
            t += evaluate(m)
        return t


def message(*msg: dict[str, Any]):
    print(text(list(msg)))


def style(
    text: str,
    color: str = "none",
    background: str = "none",
    bold: bool = False,
    underline: bool = False,
    darken: bool = False,
    header: bool = False,
):
    return {
        "text": text,
        "color": color,
        "background": background,
        "bold": bold,
        "underline": underline,
        "darken": darken,
        "header": header,
    }


import time

_name = "Main"


def _time(epoch: float):
    day, month, day_num, hhmmss, year = time.ctime(epoch).split(" ")
    return hhmmss


def _log(level: str, text: str, format: tuple[str, ...], color: str):
    message(
        {
            "text": "%s [%s][%s]: %s"
            % (_time(time.time()), _name, level, text % format),
            "color": color,
        }
    )


def _log_function(level: str, color: str, names: int = 2):
    func = lambda msg, *format: _log(level, msg, format, color)
    return [func for _ in range(names)]


deb, debug = _log_function("Debug", "green", 2)
inf, info = _log_function("Info", "white", 2)
warn, warning = _log_function("Warn", "yellow", 2)
err, error = _log_function("Error", "red", 2)
crit, critical = _log_function("Critical", "magenta", 2)

from tkinter.messagebox import showerror
import sys

def exception(
    title: str, message: str, possible_causes: list[str], level: int, code: int
):
    showerror(
        title,
        "code:%s - level:%s,\n%s\nPossible causes: %s."
        % (code, level, message, ", ".join(possible_causes)),
        icon="error",
    )

class LiminalClientException(Exception):
    code = 0
    def __init__(self, title:str, level:int, *args: object, possible_causes:list[str]=["None provided"]) -> None:
        self.title = title
        self.level = level
        self.message = "\n".join(map(lambda x: str(x),args))
        self.possible_causes = possible_causes

    def __str__(self) -> str:
        critical("title: %s, level: %s, %s",self.title,self.level,self.message)
        exception(self.title,self.message,self.possible_causes,self.level,self.code)
        return "<%s> title: %s, code:%s, level: %s, %s"%(type(self).__name__, self.title,self.code,self.level,self.message)

