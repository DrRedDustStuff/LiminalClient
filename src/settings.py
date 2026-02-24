from customtkinter import CTkFrame, CTkScrollableFrame, CTkLabel, CTkButton

from . import data, logger

class Setting:
    def __init__(self, frame, name:str, action_mappings:dict[str,list[dict[str,str]]]) -> None:
        self.frame = frame
        self.name = name
        self.variants: dict[str,int] = {}
        self.am = action_mappings

    def add(self, name:str,index:int):
        self.variants.update({name:index})
        return self

    def build(self):
        f = CTkFrame(self.frame)
        f.pack(padx=15,pady=2, side="top", fill="x")

        CTkLabel(f,text=self.name, font=("Arial", 14)).pack(padx=6,pady=4, side="left")

        for n,i in self.variants.items():
            CTkButton(f,0, text=n, font=("Arial", 14, "bold"), command=lambda: self.change_keybind(n,i)).pack(padx=6,pady=4, side="right")
        
        return self
        
    def change_keybind(self, name:str, index:int):
        logger.info(f"Changing keybind '{self.name}' for input type '{name}'")

class SettingsManager:
    def __init__(self, frame:CTkFrame) -> None:
        self.frame = frame
        self.scroll_frame = CTkScrollableFrame(frame, fg_color="transparent")
        self.scroll_frame.place(relwidth=1,relheight=1)
        self.action_mappings: dict[str, list[dict[str,str]]] = {}

        self.settings: dict[str,Setting] = {}

        self._category = ""

        self.widgets()

    def read(self):
        with open(data.etb_input, "r", encoding="utf-8") as r:
            text = r.read()
            indices = {}
            for line in text.split("[/Script/Engine.InputSettings]\n")[1].split("\n"):
                if line.strip() == "": continue
                t,v = line.split("=",1)
                if t != "ActionMappings": continue
                vals = v[1:-1].split(",")
                action_name = vals[0].split("=",1)[1][1:-1]
                if not action_name in self.action_mappings:
                    self.action_mappings.update({action_name:[{}]})
                    indices[action_name] = 0
                else:
                    self.action_mappings[action_name].append({})
                    indices[action_name] += 1
                for val in vals[1:]:
                    k,w = val.split("=",1)
                    self.action_mappings[action_name][indices[action_name]].update({k:w})

    def write(self):
        with open(data.etb_input, "w", encoding="utf-8") as w:
            text = "[/Script/Engine.InputSettings]\n"
            for action_name, attrs in self.action_mappings.items():
                for i in attrs:
                    attrs_list = []
                    for n,v in i.items(): attrs_list.append(n+"="+v)
                    attrs_text = ",".join(attrs_list)
                    text += f'ActionMappings=(ActionName="{action_name}",{attrs_text})\n'
                    print(f'- Out: ActionMappings=(ActionName="{action_name}",{attrs_text})')
            w.write(text)
    
    def widgets(self):
        self.category("DISCLAIMER:\nCurrently in the works")

        

    def category(self, name:str):
        self._category = name

        CTkLabel(self.scroll_frame, text=name, font=("Arial", 18, "bold")).pack(padx=6,pady=8, side="top", fill="x")

    def setting(self, name:str):
        kb = Setting(self.scroll_frame, name, self.action_mappings)
        self.settings.update({name:kb})
        return kb