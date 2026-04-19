from customtkinter import CTkFrame, CTkScrollableFrame, CTkLabel, CTkButton, ThemeManager, AppearanceModeTracker, get_appearance_mode
from typing import Callable, Any
from . import data, logger, resource
from tkinter import Misc
import os

class Setting:
    def __init__(self, frame, name:str) -> None:
        self.frame = frame
        self.name = name
        self.funcs: dict[str,tuple[type,Any]] = {}

    def add(self, name:str, cls:type=CTkButton, **kw):
        self.funcs.update({name:(cls,kw)})
        return self

    def build(self, func:Callable):
        f = CTkFrame(self.frame)
        f.pack(padx=15,pady=2, side="top", fill="x")

        CTkLabel(f,text=self.name, font=("Arial", 14)).pack(padx=6,pady=4, side="left")
        objs = {}
        for n,(cls,kw) in self.funcs.items():
            o = cls(master=f,**kw)
            o.pack(padx=6,pady=4, side="right")
            objs.update({n:o})
        
        func(objs)

        return self


class SettingsManager:
    def __init__(self, frame:CTkFrame, root:Misc) -> None:
        self.frame = frame
        self.scroll_frame = CTkScrollableFrame(frame, fg_color="transparent")
        self.scroll_frame.place(relwidth=1,relheight=1)

        self.settings: dict[str,Setting] = {}

        self._category = ""

        self.widgets(root)

    def read(self):
        with open(data.etb_input, "r", encoding="utf-8") as r:
            ...

    def write(self):
        with open(data.etb_input, "w", encoding="utf-8") as w:
            ...
    
    def widgets(self, root:Any):
        self.category("Visuals")

        # Theme
        theme_buttons: dict[str, CTkButton] = {}
        def select_theme(btns:dict[str,CTkButton]|None=None):
            global theme_buttons
            if btns: theme_buttons = btns
            for n,btn in theme_buttons.items():
                if "_" + n == data.theme:
                    btn.configure(fg_color=ThemeManager.theme["CTkButton"]["hover_color"][AppearanceModeTracker.appearance_mode])
                else:
                    btn.configure(fg_color=ThemeManager.theme["CTkButton"]["fg_color"][AppearanceModeTracker.appearance_mode])
        def set_theme(name:str):
            def st():
                print("Set theme to:",name)
                data.theme = name
                select_theme()
            return lambda: st()

        sett = self.setting("Theme (Requires restart)")
        for t in os.listdir(resource.get_path("theme/")):
            theme = t[:-5]
            if theme[0] == "_":
                sett.add(theme[1:], CTkButton, width=0,font=("Arial", 14, "bold"),text=theme[1:],command=set_theme(theme))
        sett.build(select_theme)
        
        # Appearance mode
        am_buttons = {}
        def select_am(btns:dict[str,CTkButton]|None=None):
            global am_buttons
            if btns: am_buttons = btns
            for n,btn in am_buttons.items():
                if n == get_appearance_mode().capitalize():
                    btn.configure(fg_color=ThemeManager.theme["CTkButton"]["hover_color"][AppearanceModeTracker.appearance_mode])
                else:
                    btn.configure(fg_color=ThemeManager.theme["CTkButton"]["fg_color"][AppearanceModeTracker.appearance_mode])
        def set_am(name:str):
            def sam():
                AppearanceModeTracker.set_appearance_mode(name)
                select_am()
            return lambda: sam()

        (self.setting("Appearance mode")
         .add("Light", width=0,font=("Arial", 14, "bold"),text="Light",command=set_am("light"))
         .add("Dark", width=0,font=("Arial", 14, "bold"),text="Dark",command=set_am("dark"))
         .add("System", width=0,font=("Arial", 14, "bold"),text="System",command=set_am("system"))
         .build(select_am))
        
        self.category("Misc")

        (self.setting("Operations")
         .add("Restart", width=0,font=("Arial", 14, "bold"),text="Restart",command=lambda:root.restart())
         .build(lambda btns:None))
        

    def category(self, name:str):
        self._category = name

        CTkLabel(self.scroll_frame, text=name, font=("Arial", 18, "bold")).pack(padx=6,pady=8, side="top", fill="x")

    def setting(self, name:str):
        kb = Setting(self.scroll_frame, name)
        self.settings.update({name:kb})
        return kb