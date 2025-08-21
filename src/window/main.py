import customtkinter as ctk
from typing import Literal
from PIL import Image

from window.settings import PSettings
from window.home import PHome
from window.modpack import PModpack
from window.modpage import PModpage

from window.mod_manager.mod import Mod

class Anchor:
    North:Literal["n"]="n"
    NorthEast:Literal["ne"]="ne"
    East:Literal["e"]="e"
    SouthEast:Literal["se"]="se"
    South:Literal["s"]="s"
    SouthWest:Literal["sw"]="sw"
    West:Literal["w"]="w"
    NorthWest:Literal["nw"]="nw"

import ctypes

# Constants from Win32 API
GWL_EXSTYLE = -20
WS_EX_APPWINDOW = 0x00040000
WS_EX_TOOLWINDOW = 0x00000080

# helper
def get_theme_color(color:list[str]) -> str:
    return color[0] if ctk.get_appearance_mode() == "dark" else color[1]

# Main window
class Main(ctk.CTk):
    def __init__(self, fg_color=None, **kwargs):
        super().__init__(fg_color=fg_color, **kwargs)
        self.theme_manager = ctk.ThemeManager()

        self.iconbitmap("./files/icon.ico")
        self.title("Neo EML")
        self.geometry("1200x800")
        self.resizable(True, True)
        self.minsize(800, 500)

        self.container_frame = ctk.CTkFrame(self, fg_color=get_theme_color(["gray78", "gray24"]))
        self.container_frame.place(x=0,y=0, relwidth=1,relheight=1)

        self._drag_data = {"x": 0, "y": 0} # contains x/y position of the window

        # Custom title-bar
        self.overrideredirect(True)
        self.attributes("-transparentcolor", "white")
        self.configure(bg="white")
        self.force_taskbar_icon()
        self.attributes("-topmost", True)
        self.after(10, lambda: self.attributes("-topmost", False))

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

    def create_widgets(self, master, start_x=80, start_y=42):
        # Custom top bar
        self.top_bar = ctk.CTkFrame(master, height=50, fg_color="transparent")
        self.top_bar.place(x=0, y=0, relwidth=1)

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
        self.tab_frame = ctk.CTkFrame(master, width=50, fg_color="transparent")
        self.tab_frame.place(x=5, y=42, relheight=0.9)  # Move down to avoid overlap with top bar

        self.btn_home = ctk.CTkButton(self.tab_frame, width=2, text="Home", command=lambda: self.show_tab("Home"))
        self.btn_home.pack(fill="x", pady=(0,5))

        self.btn_settings = ctk.CTkButton(self.tab_frame, width=2, text="Settings", command=lambda: self.show_tab("Settings"))
        self.btn_settings.pack(fill="x", pady=5)

        self.btn_modpack = ctk.CTkButton(self.tab_frame, width=2, text="Modpack", command=lambda: self.show_tab("Modpack"))
        self.btn_modpack.pack(fill="x", pady=5)

        # Content frame scaling from (start_x, start_y) to bottom-right
        self.content_frame = ctk.CTkFrame(master, fg_color="transparent")
        self._place_content_frame(start_x, start_y)  # Move down for top bar
        self.bind("<Configure>", lambda event: self._place_content_frame(start_x, start_y))

        self.show_tab("Settings")

    def _place_content_frame(self, start_x, start_y):
        win_w: int = self.winfo_width()
        win_h: int = self.winfo_height()
        if win_w < start_x + 10 or win_h < start_y + 10:
            return
        rwidth: float = (win_w - start_x) / win_w
        rheight: float = (win_h - start_y) / win_h
        self.content_frame.place(x=start_x, y=start_y, relwidth=rwidth, relheight=rheight)

    def show_tab(self, tab_name, mod:Mod | None = None):
        print("Tab request for",tab_name)
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        if tab_name == "Home":
            PHome(self.content_frame).place(relx=0, rely=0, relwidth=1, relheight=1)
        elif tab_name == "Settings":
            PSettings(self.content_frame).place(relx=0, rely=0, relwidth=1, relheight=1)
        elif tab_name == "Modpack":
            PModpack(self.content_frame).place(relx=0, rely=0, relwidth=1, relheight=1)
        elif tab_name == "Modpage" and mod:
            PModpage(self.content_frame, mod).place(relx=0, rely=0, relwidth=1, relheight=1) 


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