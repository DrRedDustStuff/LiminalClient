from typing import Any, Mapping

from customtkinter import CTkFrame, CTkScrollableFrame, CTkLabel, CTkButton, CTkToplevel, CTkOptionMenu

from . import data, logger

keys: list[tuple[str,...]] = [tuple(i.split(",", 1)) for i in open("resources/keys.txt","r", encoding="utf-8").read().split("\n")]

class KeybindSelectWindow(CTkToplevel):
    def __init__(self, master=None) -> None:
        super().__init__(master)
        x,y = data.window_pos
    
        self.geometry(f"450x200+{self.winfo_screenwidth()//2-225//2}+{self.winfo_screenheight()//2-100/2}")
        self.resizable(False,False)

        self.withdraw()
        self.overrideredirect(True)

        self.configure(fg_color="black")

        self.frame = CTkFrame(self, bg_color="black", corner_radius=20, fg_color="gray17", border_width=2)
        self.frame.pack(anchor="center", fill="both", expand=True, padx=2,pady=2)

        self.wm_attributes("-transparentcolor", "black")

        self._choices: dict[str,str] = {}
        self._names: dict[str,str] = {}
        self.keybinds: dict[str,Any] = {}

        self.keybind:Any = None
        self.index = 0
        self.btn:CTkButton|None = None

    def add(self,name:str,id:str):
        self._choices.update({name:id})
        self._names.update({id:name})
        return self

    def select(self, choice:str):
        print(f"Selected key {choice} Input:{self._choices[choice]}")
        self.s.set(choice)
        self.hide()

    def submit(self):
        self.btn.configure(text=self.keybind.name+f" ({self._names[self.keybind.am[self.keybind.name][self.index]["Key"]]})") # type: ignore

    def widgets(self, master):
        self.header = CTkLabel(master, text="<Header:Key>", font=("Arial", 32, "bold"))
        self.header.pack(side="top", anchor="n", padx=15,pady=5, fill="x", expand=True)

        self.s = CTkOptionMenu(master, values=[n for n,i in self._choices.items()])
        self.s.pack(side="left", anchor="n", padx=15,pady=15, fill="x", expand=True)

        self.submit_button = CTkButton(master, width=0, text="Submit", font=("Arial", 16, "bold"), command=self.submit)
        self.submit_button.pack(side="right", anchor="n", padx=(4,15),pady=15, fill="x", expand=True)

        self.cancel_button = CTkButton(master, width=0, text="Cancel", font=("Arial", 16, "bold"), command=self.hide)
        self.cancel_button.pack(side="right", anchor="n", padx=(15,4),pady=15, fill="x", expand=True)

    def show(self, a, i:int, btn:CTkButton):
        self.keybind = a
        self.index = i
        self.btn = btn
        self.header.configure(text=f"{self.keybind.name}")
        self.select(self._names[self.keybind.am[self.keybind.name][self.index]["Key"]])
        self.deiconify()

    def hide(self):
        self.wm_withdraw()

class Keybind:
    def __init__(self, frame, name:str, id:str, action_mappings:dict[str,list[dict[str,str]]], ksw:KeybindSelectWindow) -> None:
        self.frame = frame
        self.id = id
        self.name = name
        self.variants: dict[str,int] = {}
        self.am = action_mappings
        self.ksw = ksw

        self.l = None

    def add(self, name:str,index:int):
        self.variants.update({name:index})
        return self

    def build(self):
        f = CTkFrame(self.frame)
        f.pack(padx=15,pady=2, side="top", fill="x")

        self.l = CTkLabel(f,text=self.name, font=("Arial", 14, "bold"))
        self.l.pack(padx=12,pady=4, side="left")

        for n,i in self.variants.items():
            b = CTkButton(f,0, text=n+f" ({self.ksw._names[self.am[self.id][i]["Key"]]})", font=("Arial", 14, "bold"))
            b.configure(command=lambda: self.change_keybind(n,i, b))
            b.pack(padx=6,pady=4, side="right")
            
        return self
    
    def update(self, name:str, index, to:dict[str,str]):
        self.am[name][index].update(to)
        
    def change_keybind(self, name:str, index:int, btn:CTkButton):
        logger.info(f"Changing keybind '{self.name}' for input type '{name}'")
        self.ksw.show(self, index, btn)

class KeybindsManager:
    def __init__(self, frame:CTkFrame) -> None:
        self.frame = frame
        self.scroll_frame = CTkScrollableFrame(frame, fg_color="transparent")
        self.scroll_frame.place(relwidth=1,relheight=1)
        self.action_mappings: dict[str, list[dict[str,str]]] = {}

        self.ksw = KeybindSelectWindow(self.frame)
        for n,i in keys:
            print(f"Name:{n} Key:{i}")
            self.ksw.add(n,i)
        self.ksw.widgets(self.ksw.frame)

        self.keybinds: dict[str,Keybind] = {}

        self._category = ""

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
        self.category("Menu")
        (self.keybind("Back","Back")
         .add("Keyboard", 0)
         .build()
        )

        self.category("Movement")
        (self.keybind("Move forward", "DPadUp")
         .add("Keyboard", 0)
         .build()
        )
        (self.keybind("Move backward", "DpadDown")
         .add("Keyboard", 0)
         .build()
        )
        (self.keybind("Move left", "DPadLeft")
         .add("Keyboard", 0)
         .build()
        )
        (self.keybind("Move right", "DPadRight")
         .add("Keyboard", 0)
         .build()
        )

        (self.keybind("Crouch / Sneak","Crouch")
         .add("Keyboard", 1)
         .build()
        )
        (self.keybind("Jump","Jump")
         .add("Keyboard", 1)
         .build()
        )
        (self.keybind("Sprint / Run","Sprint")
         .add("Keyboard", 1)
         .build()
        )

        self.category("Multiplayer")
        (self.keybind("Chat","Chat")
         .add("Keyboard", 0)
         .build()
        )
        (self.keybind("Show Player List","PlayerList")
         .add("Keyboard", 1)
         .build()
        )
        (self.keybind("Show ID","ShowIDCard")
         .add("Keyboard", 0)
         .build()
        )
        (self.keybind("Talk","Talk")
         .add("Keyboard", 1)
         .build()
        )

        self.category("Misc")
        (self.keybind("Interact / Pick up","Interact")
         .add("Keyboard", 1)
         .build()
        )
        (self.keybind("Use Item","Use")
         .add("Keyboard", 1)
         .build()
        )

    def category(self, name:str):
        self._category = name

        CTkLabel(self.scroll_frame, text=name, font=("Arial", 18, "bold")).pack(padx=6,pady=8, side="top", fill="x")

    def keybind(self, name:str, id:str):
        kb = Keybind(self.scroll_frame, name,id, self.action_mappings, self.ksw)
        self.keybinds.update({name:kb})
        self.ksw.keybinds.update({name:kb})
        return kb