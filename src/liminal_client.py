from customtkinter import CTk, CTkLabel, CTkButton, CTkSwitch, CTkFrame, BooleanVar
from customtkinter.windows.widgets.core_widget_classes.ctk_base_class import CTkBaseClass

from tkinter import filedialog, messagebox

from tkinter import Misc

from . import data, logger, resource

from .core.game_manager import GameManager
from .core.mod import Mod

class LiminalClient(CTk):
    def __init__(self):
        super().__init__()
        logger.info("Starting Liminal Client")
        self.game_manager = GameManager()

        self.widget_manager: dict[str,CTkBaseClass] = {}
        self.mod_widget_manager: dict[str, CTkFrame] = {}
        self.root = CTkFrame(self)
        self.root.place(x=0,y=0,relwidth=1,relheight=1)
        self.widgets(self.root)
        self.conf()

        data.load()
        self.game_manager.find_game()
        self.on_found()

        self.title(f"Liminal Client - {data.version}")
        self.minsize(850,550)
        self.geometry(f"850x550+{self.winfo_screenwidth()//2-425}+{self.winfo_screenheight()//2-275}")

        self.do_splash = True
        self.splash_state = 0
        self.time = 0
        self.splash()

    def splash(self):
        self.time += 0.01
        if self.do_splash:
            if self.splash_state == 0:
                if self.time >= 1:
                    self.splash_state = 1
                    self.time = 0
                self.splash_header.configure(False, text_color=f"#{"".join([hex( int( 24.1*( self.time*10 )+15 ) )[2:] for _ in range(3)])}")
            elif self.splash_state == 1:
                if self.time >= 0.5:
                    self.splash_state = 2
                    self.time = 0
            elif self.splash_state == 2:
                if self.time >= 0.8:
                    self.splash_state = 1
                    self.time = 0
                    self.do_splash = False
                self.splash_header.configure(False, text_color=f"#{"".join([hex( 256-int( 25.6*( self.time*10 ) ) )[2:] for _ in range(3)])}")
            self.after(10,self.splash)
        else:
            self._splash.place_forget()

    def on_found(self):
        if data.found:
            self.find_mods()
            return
        self.after(50, self.on_found)

    def widgets(self, master:Misc):
        # splash widgets
        self._splash = CTkFrame(self, corner_radius=0, fg_color="#000000")
        self._splash.place(x=0,y=0,relwidth=1,relheight=1)
        self._splash.propagate(False)

        self._splash.lift(master)

        self.splash_header = CTkLabel(self._splash, text="Made by\nLiminal Lab", text_color="#000000", fg_color="#000000", font=("Arial", 24, "bold"))
        self.splash_header.place(x=0,y=0,relwidth=1,relheight=0.8)

        self.splash_text = CTkLabel(self._splash, text=("First time?" if data.first_time else "Welcome back"), fg_color="#000000", font=("Arial", 14, "bold"))
        self.splash_text.place(relx=0.5,rely=1, relwidth=1,relheight=0.2, anchor="s")
        
        # normal

        self.add("title", CTkLabel(master)
            ).pack(anchor="n", fill="x", padx=8, pady=5, side="top")

        self.add("options_frame", CTkFrame(master)
            ).pack(anchor="n", fill="x", padx=32, pady=8, side="top")
        
        self.add("rg_button", CTkButton(self.get("options_frame"), command=self.game_manager.start_game)
            ).pack(anchor="n", padx=8, pady=8, side="right")
        
        self.add("fm_button", CTkButton(self.get("options_frame"), command=self.find_mods)
            ).pack(anchor="n", padx=8, pady=8, side="left")
        
        self.add("im_button", CTkButton(self.get("options_frame"), command=self.import_mod)
            ).pack(anchor="n", padx=8, pady=8, side="left")
        
        self.add("mods_frame", CTkFrame(master)
            ).pack(anchor="n", fill="both", padx=32, pady=8, side="top", expand=True)


    def find_mods(self):
        for n,w in self.mod_widget_manager.items(): w.destroy()
        self.mod_widget_manager.clear()

        for n,m in self.game_manager.find_mods().items():
            self.mod_widget_manager.update({n:self.mod_widget(m)})

    def mod_widget(self, mod:Mod):
        mw = CTkFrame(self.get("mods_frame"))
        mw.pack_propagate(True)
        mw.pack(side="top", padx=8, pady=8, fill="x")
        CTkLabel(mw, text=mod.name, font=("Arial", 18, "bold")
            ).pack(side="left", anchor="w", padx=4,pady=4)
        CTkSwitch(mw, text="", width=24, height=24, command=mod.toggle,
                variable=BooleanVar(self, mod.enabled)
            ).pack(side="right", anchor="e", padx=4,pady=4)
        CTkButton(mw, text="Delete", width=50, font=("Arial", 14, "bold"),
                command=lambda:self.delete_mod(mod)
            ).pack(side="right", anchor="e", padx=4,pady=4)
        return mw
    
    def delete_mod(self, mod:Mod):
        logger.info(f"Deleting mod {mod}")
        mod.delete()
        self.find_mods()

    def import_mod(self):
        path = filedialog.askopenfilename(title="Import mod", filetypes=[("UE Mod file","*.pak")])
        if path == "": return
        self.game_manager.import_mod(path)
        self.find_mods()

    def conf(self):
        style = resource.open_json("style")
        for k,d in style.copy().items():
            if d.get("parent"):
                parent = style[d["parent"]]
                d.pop("parent")
            else:
                parent = {}
            d.update(parent)
            if "font" in d:
                f = list(d.copy()["font"])
                d.update({"font":tuple(f)})
        for k,d in style.items():
            if k in self.widget_manager:
                self.widget_manager[k].configure(False, **d)

    def add(self, name:str, widget:CTkBaseClass):
        self.widget_manager.update({name:widget})
        return widget
    
    def get(self, name:str):
        return self.widget_manager[name]

    def exit(self):
        logger.info("Stopping Liminal Client")
        data.save()


