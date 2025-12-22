import customtkinter as ctk
from customtkinter import CTkFont, CTkImage
import tkinter as tk
from typing import Literal, Tuple, Any, Callable, Iterable
from PIL import Image
from time import sleep
from threading import Thread

from .translation_manager import TranslationManager, TLabel, TButton
from .style_manager import StyleManager
from .style_manager.tkstyle_reader import TKStyle, os_name
from .container import Settings
from mod_manager.mod import ModManager

def sleepm(ms:int) -> None:
    if ms > 0:
        sleep(ms / 1000)
    else:
        print("nice try! you cant make me divide by zero")

from .pages import *

from mod_manager.mod import Mod

class Anchor:
    North:Literal["n"]="n"
    NorthEast:Literal["ne"]="ne"
    East:Literal["e"]="e"
    SouthEast:Literal["se"]="se"
    South:Literal["s"]="s"
    SouthWest:Literal["sw"]="sw"
    West:Literal["w"]="w"
    NorthWest:Literal["nw"]="nw"
    Center:Literal["center"]="center"

import ctypes
from ctypes import wintypes

# ------------- #
# Helper        #
def get_file(file:str) -> str:
    return f"files/{file}"

def get_image(file:str, size:tuple[int, int], ld:bool = False) -> CTkImage:
    """get image by file, file does not include .png
    <br>ld: has light and dark version, if true -light or -dark is appended *(Not implemented)"""
    return CTkImage(Image.open(f"files/images/{file}.png"), Image.open(f"files/images/{file}.png"), size)

def color_by_mode(color:list[str] | tuple[str, str], mode:Literal["light", "dark"] | str):
    return color[0] if mode == "light" else color[1]

def percentage_lose_precision(value:float) -> float:
    return round(value * 1_000) / 1_000

def set_app_id(app_id: str):
    """Sets a Windows AppUserModelID for taskbar grouping and notifications."""
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(wintypes.LPCWSTR(app_id))

# Constants
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
SWP_FRAMECHANGED = 0x0020

class FTFrame(ctk.CTkFrame):
    def __init__(self, master: Any, 
                 sx: int = 200, sy: int = 200,
                 ex: int | None = None, ey: int | None = None,   # absolute mode
                 ex_offset: int | None = None, ey_offset: int | None = None,  # offset mode
                 corner_radius: int | str | None = None, 
                 border_width: int | str | None = None,
                 bg_color: str | Tuple[str, str] = "transparent", 
                 fg_color: str | Tuple[str, str] | None = None, 
                 border_color: str | Tuple[str, str] | None = None,
                 background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, 
                 overwrite_preferred_drawing_method: str | None = None, 
                 **kwargs):
        
        super().__init__(master, 
                         corner_radius=corner_radius,
                         border_width=border_width,
                         bg_color=bg_color,
                         fg_color=fg_color,
                         border_color=border_color,
                         background_corner_colors=background_corner_colors,
                         overwrite_preferred_drawing_method=overwrite_preferred_drawing_method,
                         **kwargs)

        # Save config
        self.sx, self.sy = sx, sy
        self.ex, self.ey = ex, ey
        self.ex_offset, self.ey_offset = ex_offset, ey_offset

        self._place_frame()

        # Auto-update on resize
        self.master.bind("<Configure>", lambda event: self.after(20, self._place_frame))

    def _place_frame(self):
        win_w = self.master.winfo_width()
        win_h = self.master.winfo_height()

        if win_w < self.sx + 10 or win_h < self.sy + 10:
            return

        # resolve ex
        if self.ex is not None:
            ex = self.ex
        else:
            ex = win_w - (self.ex_offset or 0)

        # resolve ey
        if self.ey is not None:
            ey = self.ey
        else:
            ey = win_h - (self.ey_offset or 0)

        # relative sizes
        rwidth = (ex - self.sx) / win_w
        rheight = (ey - self.sy) / win_h

        self.place(x=self.sx, y=self.sy, relwidth=rwidth, relheight=rheight)

# Loading window should be implemented
class LoadingWindow(ctk.CTkFrame):
    def __init__(self, master, color_mode:Literal["light", "dark"] | str, **kwargs):
        super().__init__(master, fg_color="gray1", **kwargs)

        self.f_main = ctk.CTkFrame(self, corner_radius=20, border_color=color_by_mode(["#e0e0e0", "#202020"], color_mode), border_width=5, bg_color="gray1", fg_color=color_by_mode(["#c0c0c0", "#303030"], color_mode))
        self.f_main.place(relx=0.5,rely=0.5, relwidth=0.9,relheight=0.9, anchor=Anchor.Center)

        self.content_master = ctk.CTkFrame(self.f_main, corner_radius=0, bg_color="transparent", fg_color="transparent")
        self.content_master.place(relx=0.5,rely=0.5, relwidth=0.91,relheight=0.91, anchor=Anchor.Center)
        
        self.create_widgets(self.content_master)

        self.lift()
        self.after(10, self.focus_force)

    def create_widgets(self, master:Any):
        # for padding % use formula: 1 - padding * 2, returns size (e.g.: padding w% returns width%, 12.5% returns 75%) so, use as relwidth value
        # padding should be floated first (e.g.: 45% -> 0.45) or (percent / 100 = floated_percent)

        # top 25% height 12.5% padding (h/w) Label: Loading
        self.title_label = ctk.CTkLabel(master, text="<Unset>", 
                                        font=CTkFont("Arial", 42, "bold")
                                        )
        self.title_label.place(anchor=Anchor.North, relx=0.5,rely=0.125, relwidth=0.75, relheight=0.25)

        # bottom 50% height 50% ypos 6.25% padding (w) Frame: info
        self.info_container = ctk.CTkFrame(master, bg_color="transparent", fg_color="transparent")
        self.info_container.place(anchor=Anchor.North, relx=0.5,rely=0.50, relwidth=0.875, relheight=0.5)

        # in Frame: info top 50% height 100% width Label: loading info
        self.ic_l_loading_info = ctk.CTkLabel(self.info_container, text="",
                                              font=CTkFont("Roboto", 28, "bold"))
        self.ic_l_loading_info.place(anchor=Anchor.North, relx=0.5,rely=0, relwidth=1,relheight=0.375)
        self.ic_l_sub_info = ctk.CTkLabel(self.info_container, text="",
                                          font=CTkFont("Roboto", 20, "normal", "italic"))
        self.ic_l_sub_info.place(anchor=Anchor.North, relx=0.5,rely=0.375, relwidth=1, relheight=0.125)

        # in Frame: info bottom 12.5% height 0.75 ypos 100% width center anchor LoadingBar: loading percentage
        self.lp_value = ctk.DoubleVar(self, 0, "LoadingProgressPercentage")
        self.ic_lb_loading_percentage = ctk.CTkProgressBar(self.info_container, variable=self.lp_value)
        self.ic_lb_loading_percentage.place(anchor=Anchor.Center, relx=0.5,rely=0.625, relwidth=1, relheight=0.125)

    def add_percentage(self, amount:int):
        old_percent = self.lp_value.get()
        if self.lp_value.get() < 100:
            self.lp_value.set(percentage_lose_precision(self.lp_value.get() + (amount / 100) if amount > 0 else 0))
        print(f"{old_percent * 100}% -> {self.lp_value.get() * 100}%")
    
    def set_percentage(self, value:int):
        print(f"{self.lp_value.get() * 100}% -> {value}")
        self.lp_value.set((value / 100) if value > 0 else 0)
    
    def update_loading_info(self, info:str):
        self.ic_l_loading_info.configure(text=info)
    def update_sub_info(self, info:str):
        self.ic_l_sub_info.configure(text=info)
    
    def done(self):
        print("done loading")
        self.set_percentage(1)
        self.destroy()

# Main window
class Main(ctk.CTk):
    # ---------------- #
    # Thread-safety
    # Thread Misc

    def wait_on_thread(self, thread:Thread):
        if thread.is_alive():
            self.after(20, lambda: self.wait_on_thread(thread))
        else:
            print(f"Thread {thread.name} is done")
    
    def on_thread_dead(self, thread:Thread, func:Callable):
        if thread.is_alive():
            self.after(20, lambda: self.on_thread_dead(thread, func))
        else:
            print(f"Thread {thread.name} is done")
            func()

    # ---------------- #
    # Main

    def __init__(self, **kwargs):
        super().__init__(fg_color="gray1", **kwargs)

        set_app_id("LiminalClient.Main")

        self.settings = Settings("s.inf")

        self.theme_manager = ctk.ThemeManager()
        self.translation_manager = TranslationManager(self.settings.lang, "files/translation")
        self.style: TKStyle = TKStyle(f"./files/style/{os_name()}.tks").load()
        self.mod_manager = ModManager("./files/modpacks/mods/")

        self.loading_window = LoadingWindow(self, self._get_appearance_mode())
        self.loading_window.title_label.configure(text=self.translation_manager.get_raw("loading.header"))
        self.loading_window.update_loading_info(self.translation_manager.get_raw("loading.initializing")) # Initializing
        self.loading_window.place(relx=0,rely=0,relheight=1,relwidth=1)

        self.iconbitmap("./files/icon.ico")
        self.title("Liminal Client")
        self.geometry("1200x850+20+20")
        self.resizable(True, True)
        self.minsize(800, 500)

        self._drag_data: dict[str, int] = {"x": 0, "y": 0} # contains x/y position of the window

        # Custom title-bar
        self.overrideredirect(True)
        self.after(20, self.force_taskbar_icon)
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))
        self.configure(bg="gray1")
        self.configure(fg="gray1")
        self.wm_attributes("-transparentcolor", "gray1")

        self.container_frame = ctk.CTkFrame(self,
                                            fg_color="gray25",#self._apply_appearance_mode(["gray78", "gray24"]),
                                            corner_radius=8
                                            )
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.loading_window.update_loading_info(self.translation_manager.get_raw("loading.creating_widgets")) # Creating Widgets
        self.loading_window.add_percentage(25)
        self.pages: dict[Any, PHome | PModpack | PModpage | PSettings | PModDiscovery | None] = {}
        self.current_page = None
        self.create_widgets(self.container_frame)
        self.loading_window.update_loading_info(self.translation_manager.get_raw("loading.waiting_subthread")) # Waiting on Subthread
        self.loading_window.add_percentage(50)

        self.on_thread_dead(self.t_preload_pages, self.thread_preload_pages_done)
    
    def thread_preload_pages_done(self):
        self.show_page("Home")
        self.container_frame.place(relx=0,rely=0, relwidth=1,relheight=1)
        self.loading_window.update_loading_info("Waiting for container frame")
        self.loading_window.update_sub_info("")
        self.loading_window.lift(self.container_frame)
        self.translation_manager.update_text_likes()
        self.after(ms=220, func=self.container_frame.lift)
        # self.loading_window.done()

    def force_taskbar_icon(self):
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

        # Remove TOOLWINDOW (hidden from taskbar)
        style &= ~WS_EX_TOOLWINDOW
        # Add APPWINDOW (visible in taskbar)
        style |= WS_EX_APPWINDOW

        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)

        # Refresh the window style
        ctypes.windll.user32.SetWindowPos(
            hwnd, 0, 0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED
        )

    def create_widgets(self, master:Any):
        # to increase loading times the content frame is placed before the top bar
        self.content_frame = FTFrame(master, sx=64, sy=48, ex_offset=4, ey_offset=4, corner_radius=20)#, bg_color="gray25")
        self.content_frame.place(rely=0, relwidth=1)

        self.loading_window.update_sub_info(self.translation_manager.get_raw("loading.creating_subthread")) # Creating Subthread
        self.t_preload_pages = Thread(target=self.preload_pages)
        self.t_preload_pages.start() # preload pages

        # Custom top bar
        self.top_bar = ctk.CTkFrame(master, height=40, corner_radius=0, fg_color="transparent")
        self.top_bar.place(relx=0.5, y=4, relwidth=0.989, anchor=Anchor.North)
        self.top_bar.pack_propagate(False)

        # Icon
        self.i_topbar_icon = ctk.CTkImage(Image.open("./files/icon.ico"),Image.open("./files/icon.ico"), (32, 32))
        self.il_topbar_icon = ctk.CTkLabel(self.top_bar, image=self.i_topbar_icon, text="")
        self.il_topbar_icon.pack(side="left", padx=5, pady=2)

        # Title
        self.title_label = ctk.CTkLabel(self.top_bar, text="Liminal Client", font=self.style.font("font"), fg_color="transparent")
        self.title_label.pack(side="left", padx=10)

        # Exit button
        self.exit_btn = ctk.CTkButton(self.top_bar, text="✕", width=30, command=self.destroy, fg_color="#c00")
        self.exit_btn.pack(side="right", padx=5, pady=5)

        # Fullscreen button
        self.full_btn = ctk.CTkButton(self.top_bar, text="⬜", width=30, command=self.toggle_fullscreen, fg_color="#666")
        self.full_btn.pack(side="right", padx=5, pady=5)

        # Drag-to-move
        self.top_bar.bind("<ButtonPress-1>", self._start_move)
        self.top_bar.bind("<B1-Motion>", self._do_move)
        self.title_label.bind("<ButtonPress-1>", self._start_move)
        self.title_label.bind("<B1-Motion>", self._do_move)

        # Vertical page buttons
        self.page_frame = FTFrame(master, sx=0,sy=48,ex=64,ey_offset=10, fg_color="transparent")
        self.page_frame.place(rely=0, relwidth=1)
        self.page_frame.pack_propagate(False)

        self.home_btn = ctk.CTkButton(self.page_frame, text="", width=2, image=get_image("home", (32,32)), command=lambda: self.show_page("Home"))
        self.home_btn.pack(pady=5, padx=5)

        self.settings_btn = ctk.CTkButton(self.page_frame, text="", width=2, image=get_image("settings", (32,32)), command=lambda: self.show_page("Settings"))
        self.settings_btn.pack(pady=5, padx=5)

        self.modpack_btn = ctk.CTkButton(self.page_frame, text="", width=2, image=get_image("modpack", (32,32)), command=lambda: self.show_page("Modpack"))
        self.modpack_btn.pack(pady=5, padx=5)

        self.mod_discovery_btn = ctk.CTkButton(self.page_frame, text="", width=2, image=get_image("mod-discovery", (32,32)), command=lambda: self.show_page("ModDiscovery"))
        self.mod_discovery_btn.pack(pady=5, padx=5)
        
    def preload_pages(self):
        self.loading_window.update_sub_info(self.translation_manager.get_raw("loading.preloading_home"))      # Preloading Home
        self.show_page("Home")                                 # load homepage
        self.loading_window.add_percentage(8)
        self.loading_window.update_sub_info(self.translation_manager.get_raw("loading.preloading_modpack"))   # Preloading Modpack
        self.show_page("Modpack", False)             # load modpack
        self.loading_window.add_percentage(8)
        self.loading_window.update_sub_info(self.translation_manager.get_raw("loading.preloading_settings"))  # Preloading Settings
        self.show_page("Settings")                             # load settings
        self.loading_window.add_percentage(8)
        self.loading_window.update_sub_info(self.translation_manager.get_raw("loading.preloading_settings"))  # Preloading Settings
        self.show_page("ModDiscovery")                             # load settings
        self.loading_window.add_percentage(8)
        self.loading_window.update_sub_info(self.translation_manager.get_raw("loading.done_preloading")) # Done Preloading, Thread Dead

    def show_page(self, page_name: Literal["Home", "Settings", "Modpack", "Modpage", "ModDiscovery"], load_mods:bool = True, mod: Mod | None = None) -> None | bool:
        print("\nPage request for", page_name)

        if page_name == self.current_page:
            print("Page already open")
            return True # thread safety

        # Hide the currently visible page
        if self.current_page in self.pages:
            page = self.pages[self.current_page]
            if page:
                print("lowering",self.current_page)
                page.lower()
        elif self.current_page == "Modpage":
            # Destroy only the dynamic Modpage
            if hasattr(self, "_current_modpage") and self._current_modpage and self._current_modpage.winfo_exists():
                self._current_modpage.destroy()
                self._current_modpage = None

        # Handle Modpage (always rebuilt)
        if page_name == "Modpage" and mod:
            frame = PModpage(self.content_frame, self.translation_manager, mod)
            frame.place()
            self._current_modpage: PModpage | None = frame
            self.current_page = "Modpage"
            return

        # Handle cached pages
        if page_name not in self.pages:
            if page_name == "Home":
                self.pages[page_name] = PHome(self.content_frame, self.translation_manager)
            elif page_name == "Settings":
                self.pages[page_name] = PSettings(self.content_frame, self.translation_manager)
            elif page_name == "Modpack":
                self.pages[page_name] = PModpack(self.content_frame, self.translation_manager, load_mods)
            elif page_name == "ModDiscovery":
                self.pages[page_name] = PModDiscovery(self.content_frame, self.translation_manager)
            else:
                return True # thread safety

        # Show cached frame (not destroyed)
        frame = self.pages[page_name]
        if frame:
            if isinstance(frame, PModpack): frame.reload_mods() # reload mods if is Modpack Page/Tab
            if frame.place_info() == {}: # if not placed yet
                print("placing",page_name)
                frame.place()
            else:
                print("lifting",page_name)
                frame.lift()
                
        self.current_page = page_name
        return True

    def toggle_fullscreen(self):
        if not hasattr(self, "_is_fullscreen"):
            self._is_fullscreen = False
        if not self._is_fullscreen:
            self._prev_geometry = self.geometry()
            self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
            self._is_fullscreen = True
        else:
            if getattr(self, "_prev_geometry", None) is not None:
                self.geometry(self._prev_geometry) # pyright: ignore[reportArgumentType]
            self._is_fullscreen = False

    def _start_move(self, event):
        self._drag_data["x"] = event.x
        self._drag_data["y"] = event.y

    def _do_move(self, event):
        x = self.winfo_pointerx() - self._drag_data["x"]
        y = self.winfo_pointery() - self._drag_data["y"]
        self.geometry(f"+{x}+{y}")
