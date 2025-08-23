import customtkinter as ctk
from typing import Literal, Tuple, Any
from PIL import Image
from time import sleep

def sleepm(ms:int):
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

# Constants from Win32 API
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

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

# Main window
class Main(ctk.CTk):
    def __init__(self, **kwargs):
        super().__init__(fg_color="gray1", **kwargs)
        self.theme_manager = ctk.ThemeManager()

        self.iconbitmap("./files/icon.ico")
        self.title("Neo EML")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.minsize(800, 500)

        self._drag_data = {"x": 0, "y": 0} # contains x/y position of the window

        # Custom title-bar
        self.overrideredirect(True)
        self.force_taskbar_icon()
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))
        self.configure(bg="gray1")
        self.configure(fg="gray1")
        self.wm_attributes("-transparentcolor", "gray1")

        self.container_frame = ctk.CTkFrame(self,
                                            fg_color="gray25",#self._apply_appearance_mode(["gray78", "gray24"]),
                                            corner_radius=8
                                            )
        self.container_frame.place(relx=0,rely=0, relwidth=1,relheight=1)
        self.pack_propagate(False)
        self.grid_propagate(False)

        self.tabs = {}
        self.current_tab = None
        self.create_widgets(self.container_frame)

    def force_taskbar_icon(self):
        hwnd = ctypes.windll.user32.GetParent(self.winfo_id())
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_EXSTYLE)

        # Remove TOOLWINDOW style (hides from taskbar)
        style &= ~WS_EX_TOOLWINDOW
        # Add APPWINDOW style (shows in taskbar)
        style |= WS_EX_APPWINDOW

        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_EXSTYLE, style)
        # Refresh window style
        ctypes.windll.user32.SetWindowPos(hwnd, 0, 0, 0, 0, 0,
                                        0x0027)  # SWP_NOMOVE|SWP_NOSIZE|SWP_NOZORDER|SWP_FRAMECHANGED

    def create_widgets(self, master):
        # Custom top bar
        self.top_bar = ctk.CTkFrame(master, height=40, corner_radius=0, fg_color="transparent")
        self.top_bar.place(relx=0.5, y=0, relwidth=0.989, anchor=Anchor.North)
        self.top_bar.pack_propagate(False)

        # Icon
        self.i_topbar_icon = ctk.CTkImage(Image.open("./files/icon.ico"),Image.open("./files/icon.ico"), (32, 32))
        self.il_topbar_icon = ctk.CTkLabel(self.top_bar, image=self.i_topbar_icon, text="")
        self.il_topbar_icon.pack(side="left", padx=5, pady=2)

        # Title
        self.title_label = ctk.CTkLabel(self.top_bar, text="Neo EML", font=("Arial", 16), fg_color="transparent")
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

        # Vertical tab buttons
        self.tab_frame = FTFrame(master, sx=0,sy=40,ex=75,ey_offset=10, fg_color="transparent")
        self.tab_frame.place(rely=0, relwidth=1)
        self.tab_frame.pack_propagate(False)

        self.btn_home = ctk.CTkButton(self.tab_frame, width=2, text="Home", command=lambda: self.show_tab("Home"))
        self.btn_home.pack(fill="x", pady=5, padx=5)

        self.btn_settings = ctk.CTkButton(self.tab_frame, width=2, text="Settings", command=lambda: self.show_tab("Settings"))
        self.btn_settings.pack(fill="x", pady=5, padx=5)

        self.btn_modpack = ctk.CTkButton(self.tab_frame, width=2, text="Modpack", command=lambda: self.show_tab("Modpack"))
        self.btn_modpack.pack(fill="x", pady=5, padx=5)

        # Content frame scaling from (start_x, start_y) to bottom-right
        self.content_frame = FTFrame(master, sx=75, sy=40, ex_offset=4, ey_offset=4, corner_radius=20)#, bg_color="gray25")
        self.content_frame.place(rely=0, relwidth=1)

        self.show_tab("Modpack")

    def show_tab(self, tab_name: Literal["Home", "Settings", "Modpack", "Modpage"], mod: Mod | None = None):
        print("Tab request for", tab_name)

        # Hide the currently visible tab
        if self.current_tab in self.tabs:
            self.tabs[self.current_tab].place_forget()
        elif self.current_tab == "Modpage":
            # Destroy only the dynamic Modpage
            if hasattr(self, "_current_modpage") and self._current_modpage and self._current_modpage.winfo_exists():
                self._current_modpage.destroy()
                self._current_modpage = None

        # Handle Modpage (always rebuilt)
        if tab_name == "Modpage" and mod:
            frame = PModpage(self.content_frame, mod)
            frame.place()
            self._current_modpage = frame
            self.current_tab = "Modpage"
            return

        # Handle cached tabs
        if tab_name not in self.tabs:
            if tab_name == "Home":
                self.tabs[tab_name] = PHome(self.content_frame)
            elif tab_name == "Settings":
                self.tabs[tab_name] = PSettings(self.content_frame)
            elif tab_name == "Modpack":
                self.tabs[tab_name] = PModpack(self.content_frame)
            else:
                return

        # Show cached frame (not destroyed)
        frame = self.tabs[tab_name]
        frame.place()
        self.current_tab = tab_name

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
