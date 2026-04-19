from typing import Any, Mapping

from customtkinter import CTkFrame, CTkScrollableFrame, CTkLabel, CTkButton, CTkToplevel, CTkOptionMenu

from . import data, logger

class GameFile:
    def __init__(self, name:str, file:str) -> None:
        pass

class GameFilesManager:
    def __init__(self, frame:CTkFrame) -> None:
        self.frame = frame
        self.scroll_frame = CTkScrollableFrame(frame, fg_color="transparent")
        self.scroll_frame.place(relwidth=1,relheight=1)
        self.action_mappings: dict[str, list[dict[str,str]]] = {}

        self._category = ""

        self.widgets()

    def widgets(self):
        self.category("DISCLAIMER:\nCurrently in the works")

    def category(self, name:str):
        self._category = name

        CTkLabel(self.scroll_frame, text=name, font=("Arial", 18, "bold")).pack(padx=6,pady=8, side="top", fill="x")

    def file(self, name:str, file:str):
        ...
