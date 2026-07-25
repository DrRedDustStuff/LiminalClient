import time
from typing import Any

from customtkinter import CTk, CTkFont
import customtkinter as ctk
from tkinter import PhotoImage, DoubleVar, Frame as TkFrame

from .ui.widgets import (
    Frame,
    ScrollableFrame,
    Label,
    Entry,
    Button,
    Slider,
    OptionMenu,
)
from .ui.mod_display import ModDisplay
from .ui.ui_manager import WidgetManager
from .datafile import Datafile

from .pages import page

from . import data
from . import resource
from . import log
from . import sound
from . import button_functions
from . import pages

from threading import Thread
from .exceptions import UnhandledCase
import requests

from .plugin.plugin_manager import PluginManager
from .plugin.plugin_event import PluginEvent

def ping_server():
    try:
        response = requests.get(data.url, timeout=3)
        if response.ok:
            data.online = True
        else:
            raise Exception(response.text)
    except requests.exceptions.Timeout as te:
        data.online = False
        print("timeout", te)
    except requests.exceptions.ConnectionError as ce:
        data.online = False
        string = str(ce)
        string = "[WinError" + string.split("[WinError", 1)[1][:-3]
        log.error("Could not ping server, %s", string)


def lerp(a: float, b: float, delta: float):
    return a + (b - a) * delta


def ease(a: float, b: float, delta: float):
    return a + (b - a) * (delta * delta * (3 - 2 * delta))


class LiminalClient:
    card_queue: list[tuple[str, str, str, float]] = []

    def load(self):
        data.initialize()
        ping_server()
        if not data.online:
            self.card(
                "Offline",
                "it seems we could not reach the Liminal Labs server",
                "#DBB449",
                3,
            )
        self.ready = True

    def card(self, title: str, text: str, color: str, hold_timeout:float=2):
        self.card_queue.append((title, text, color, hold_timeout))

    def _info_card(self, header: str, text: str, color: str, timeout:float):
        self.can_que = False
        frame = Frame(self.tk, 250, 150, corner_radius=8, fg_color="#3A3A3A")
        Frame(frame, 250, 32, corner_radius=8, fg_color=color).place(x=0, y=0)
        Frame(frame, 250, 24, fg_color="#3A3A3A").place(x=0, y=16)
        Label(
            frame, 250, 24, text=header, font=CTkFont(None, 24, "bold"), anchor="w", text_color="#F5EFD1",
        ).place(x=12, y=16).is_literal(True)
        Label(
            frame,
            250,
            25,
            text=text,
            wraplength=200,
            anchor="nw",
            justify="left",
            compound="left",
            text_color="#CFC9AA",
        ).place(x=10, y=52).is_literal(True)

        sound.notification(sound.swoosh)
        self.info_card_in(
            frame, 0, -0.5, (self.tk.winfo_height() - 4) / self.tk.winfo_height(), timeout
        )

    def info_card_in(self, card: Frame, time: float, relx: float, y: float, timeout: float):
        rx = ease(relx, 0, 0.1)
        card.place_configure(relx=rx, rely=y, x=4, anchor="sw")
        if rx > -0.001:
            self.info_card_hold(card, timeout, y)
            return
        self.tk.after(10, lambda: self.info_card_in(card, time + 0.01, rx, y,timeout))

    def info_card_hold(self, card: Frame, timeout: float, y: float):
        tm = timeout - 0.01
        if tm <= 0.001:
            self.can_que = True
            self.info_card_out(card, 0, 0, y)
            return
        self.tk.after(10, lambda: self.info_card_hold(card, tm, y))

    def info_card_out(self, card: Frame, time: float, relx: float, y: float):
        rx = ease(relx, -0.5, 0.1)
        card.place_configure(relx=rx, rely=y, x=4, anchor="sw")
        if rx < -0.499:
            card.destroy()
            return
        self.tk.after(10, lambda: self.info_card_out(card, time + 0.01, rx, y))

    def run_card_queue(self):
        if len(self.card_queue) > 0 and self.can_que:
            title, text, color, timeout = self.card_queue.pop(0)
            self._info_card(title, text, color,timeout)
        self.tk.after(10, self.run_card_queue)

    def get_time(self):
        curr = time.time()
        string = f"{(curr-self.start_time)*100:0.2f}/{(curr-self._lt)*100:0.2f}ms"
        self._lt = curr
        return string

    def __init__(self) -> None:
        log.info("Initializing LiminalClient!")
        self.start_time = time.time()
        self._lt = time.time()
        WidgetManager.load_theme()
        self.can_que = True

        pages.page.add_page = self.add_page

        log.info("(%s) Initializing CTk Window", self.get_time())
        self.tk = CTk()
        self.tk.geometry(f"1200x800")
        self.tk.minsize(1200, 800)
        self.tk.resizable(True, True)
        self.tk.iconbitmap(default=resource.path("image/icon.ico"))
        self.tk.title("Liminal Client")

        self.mods: list[ModDisplay] = []

    def start(self):
        log.info("(%s) Starting load thread", self.get_time())
        self.ready = False
        self.load_thread = Thread(target=self.load)
        self.load_thread.start()

        self.pages: dict[str, ScrollableFrame] = {}
        self._current_page: ScrollableFrame | None = None

        log.info("Finding and loading Plugins")
        PluginManager.load()
        PluginManager.load_all()
        log.info("(%s) Loading all non dynamic widgets", self.get_time())
        self.widgets(self.tk)
        self.all_widgets_loaded.call()
        log.info("(%s) Translating loaded widgets", self.get_time())
        WidgetManager.translate("en_us")
        log.info("(%s) Starting to poll card queue (every 10ms)", self.get_time())
        self.run_card_queue()
        if data.prefix == "beta":
            self.tk.after(
                10,
                lambda: self.card(
                    "Beta, (%s)" % (data.version()),
                    "Thank you for playtesting the beta version of Liminal Client! Report any bugs or errors to the Liminal Labs team.",
                    "#4FF02F",
                    7,
                ),
            )
        elif data.prefix == "early-access":
            self.tk.after(
                10,
                lambda: self.card(
                    "Early Access, (%s)" % (data.version()),
                    "Thank you for using the early access version of Liminal Client! Please report any bugs or errors to the Liminal Labs team.",
                    "#2FB9F0",
                    7,
                ),
            )

        log.info("Initializing Plugins")
        PluginManager.initialize_all()
        log.info("Starting tkinter mainloop")
        self.tk.mainloop()

    def stop(self):
        log.info("Stopping")
        log.info("Unloading all plugins")
        PluginManager.unload_all()
        PluginEvent.__check_empty__()
        self.load_thread.join()

    all_widgets_loaded: PluginEvent[()] = PluginEvent()

    def widgets(self, master):
        self.head_icon = Label(master,text="",image=resource.image("icon.png",(50,50))).place(x=5,y=2).is_literal(True)

        self.main_header = (
            Label(master, text="Liminal Client", font=CTkFont(None, 30, "bold"))
            .place(y=4, x=60)
            .is_literal(True)
        )

        self.version_label = (
            Label(
                master,
                text_color="#969696",
                text=f"v:" + data.version(),
                font=CTkFont(None, 14, "normal", "italic"),
            )
            .place(y=12, x=260)
            .is_literal(True)
        )

        self.main = Frame(master, corner_radius=24, border_width=3)
        self.main.place(x=60, y=50, relwidth=1, relheight=1)

        self.page_initialize(master)

        self._test_mods()
        

    def page_initialize(self, master):
        self.side_buttons = Frame(master, 50, 0, 0, 0, fg_color="#000000").place(
            x=5, y=60, relheight=1
        )

        for page in pages.page.pages:
            page(self.main)

        from .pages.main import Main
        self.main_frame: Main = WidgetManager.get_widget_by_id("liminal_client.main.page",Main)[1]

        self.show_page("main")

    def page_button(self,pageid: str):
        return (
            Button(
                self.side_buttons,
                00,
                50,
                8,
                2,
                text="",
                image=resource.image("pageicon/" + pageid + ".png", (30, 30)),
                command=lambda: self.show_page(pageid),
            )
            .pack(pady=(0, 5))
            .id("pagebutton_%s" % pageid)
        )

    def add_page(self, id: str, frame: ScrollableFrame):
        if id in self.pages.keys(): raise Exception("Page %s already exists"%id)
        self.pages.update({id:frame})
        self.page_button(id)

    def show_page(self, id: str):
        if id in self.pages.keys():
            if not self._current_page is None:
                if self._current_page == self.pages[id]:
                    return
                self._current_page.pack_forget()
            log.info("opening page %s", id)
            self._current_page = self.pages[id]
            self._current_page.pack(
                padx=(15, 65), pady=(5, 60 - 4), fill="both", expand=True
            )
        else:
            if hasattr(self, id + "_frame"):
                self.pages.update({id: getattr(self, id + "_frame")})
                self.show_page(id)
            else:
                raise UnhandledCase()

    def clear_mod_widgets(self):
        for _ in self.mods.copy():
            self.mods.pop(0).destroy()

    def add_mod_widget(
        self,
        id: int = 0,
        name: str = "NAME",
        creator: str = "CREATOR",
    ):
        mod_display = ModDisplay(self.main_frame.mods_frame, id, name, creator)
        self.mods.append(mod_display)
        mod_display.pack(padx=10, pady=4, fill="x")

    def _test_mods(self):
        self.add_mod_widget(0, "Interpose", "Mythical")
        self.add_mod_widget(1, "PyModMenu", "Py guy")

        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")
        self.add_mod_widget(4, "Mischievous", "Miscor")


_instance: LiminalClient | None = None

def main():
    global _instance
    _instance = LiminalClient()
    _instance.start()
    _instance.stop()

def get_instance():
    if _instance is None:
        raise Exception("Liminal Client has not been fully initialized yet")
    return _instance
