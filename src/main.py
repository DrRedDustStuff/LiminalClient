import time
from typing import Any, cast

from customtkinter import CTk, CTkFont, CTkToplevel
import customtkinter as ctk
from tkinter import PhotoImage, DoubleVar, Frame as TkFrame

from blublib.ui.widgets import (
    Frame,
    ScrollableFrame,
    Label,
    Button,
)
from blublib.ui.ui_manager import WidgetManager

from .pages import page
from log import Logger

from . import data
from blublib import resource
from blublib.resource import Identifier
from . import sound
from .stack import Stack
from . import button_functions
from . import pages
from . import liminal_lab
from . import loggers

from . import console

from threading import Thread
from .exceptions import UnhandledCase
import requests

from blublib.plugin.plugin_manager import PluginManager
from blublib.plugin.plugin_event import PluginEvent
from blublib import kv_file

import os.path

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
        if ce.response is None: return 
        
        string = ce.response.reason
        loggers.load.error("Could not ping server, %s", string)


def lerp(a: float, b: float, delta: float):
    return a + (b - a) * delta


def ease(a: float, b: float, delta: float):
    return a + (b - a) * (delta * delta * (3 - 2 * delta))


class LiminalClient:
    page_stack: Stack[str] = Stack()
    card_queue: list[tuple[str, str, str, float]] = []

    main_done_loading: PluginEvent[()] = PluginEvent()
    done_loading: PluginEvent[()] = PluginEvent()
    "called when the async load finnishes"
    def load(self):
        try:
            self.splash_screen.lift()
        except RuntimeError as re:
            print(re)
        resource.load()
        data.initialize()
        if data.console_enabled: console.initialize()
        self.main_done_loading.call()
        while not self._wlb:
            time.sleep(0.25)
        self.splash_screen.destroy()
        ping_server()
        if not data.online:
            self.card(
                "Offline",
                "it seems we could not reach the Liminal Labs server",
                "#DBB449",
                3,
            )
        else:
            loggers.load.info("Testing if all server functions available")
            versions = liminal_lab.liminal_client.get_versions()
            tags = liminal_lab.mod.tags(["all"])
        self.done_loading.call()
        
        self.ready = True


    def card(self, title: str, text: str, color: str, hold_timeout: float = 2):
        self.card_queue.append((title, text, color, hold_timeout))

    def _info_card(self, header: str, text: str, color: str, timeout: float):
        self.can_que = False
        frame = Frame(self.tk, 250, 150, corner_radius=8, fg_color="#3A3A3A")
        Frame(frame, 250, 32, corner_radius=8, fg_color=color).place(x=0, y=0)
        Frame(frame, 250, 24, fg_color="#3A3A3A").place(x=0, y=16)
        Label(frame, 250, 24, text=header, font=CTkFont(None, 24, "bold"), anchor="w", text_color="#F5EFD1").place(x=12, y=16).is_literal(True)
        Label(frame, 250, 25, text=text, wraplength=200, anchor="nw", justify="left", compound="left", text_color="#CFC9AA").place(x=10, y=52).is_literal(True)

        sound.notification(sound.swoosh)
        self.info_card_in(frame,0,-0.5,(self.tk.winfo_height() - 4) / self.tk.winfo_height(),timeout)

    def info_card_in(
        self, card: Frame, time: float, relx: float, y: float, timeout: float
    ):
        rx = ease(relx, 0, 0.1)
        card.place_configure(relx=rx, rely=y, x=4, anchor="sw")
        if rx > -0.001:
            self.info_card_hold(card, timeout, y)
            return
        self.tk.after(10, lambda: self.info_card_in(card, time + 0.01, rx, y, timeout))

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
            self._info_card(title, text, color, timeout)
        self.tk.after(10, self.run_card_queue)

    def get_time(self):
        curr = time.time()
        string = f"{(curr-self.start_time)*100:0.2f}/{(curr-self._lt)*100:0.2f}ms"
        self._lt = curr
        return string

    def __init__(self) -> None:
        loggers.main.info("Initializing LiminalClient!")
        self.start_time = time.time()
        self._lt = time.time()
        WidgetManager.load_theme()
        self.can_que = True

        loggers.main.info("(%s) Initializing CTk Window", self.get_time())
        self.tk = CTk()
        self.tk.geometry(f"1200x800")
        self.tk.minsize(1200, 800)
        self.tk.resizable(True, True)
        self.tk.iconbitmap(default=resource.path("Source","image/icon.ico"))
        self.tk.title("Liminal Client")

    def start(self):
        loggers.main.info("(%s) Starting load thread", self.get_time())
        self.splash_screen = Frame(self.tk).place(relwidth=1,relheight=1)
        self.splash(self.splash_screen)
        self.ready = False
        self.load_thread = Thread(target=self.load)
        self.load_thread.start()
        self._wlb = False

        self.pages: dict[str, page.Page] = {}
        # self.root_pages: set[str] = set()
        self._current_page: page.Page | None = None

        loggers.main.info("Finding and loading Plugins")
        PluginManager.load()
        PluginManager.load_all()
        loggers.main.info("(%s) Loading all non dynamic widgets", self.get_time())
        self.widgets(self.tk)
        self.all_widgets_loaded.call()
        self.settings.load()
        self._wlb = True
        loggers.main.info("(%s) Translating loaded widgets", self.get_time())
        WidgetManager.translate("en_us")
        loggers.main.info("(%s) Starting to poll card queue (every 10ms)", self.get_time())
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

        loggers.main.info("Initializing Plugins")
        PluginManager.initialize_all()

    def mainloop(self):
        loggers.main.info("Starting tkinter mainloop")
        self.tk.mainloop()

    def stop(self):
        loggers.main.info("Stopping")
        loggers.main.info("Un Initializing Pages")
        for pageid, page in self.pages.items():
            page.__un_init__()
        self.settings.save()
        loggers.main.info("Unloading all plugins")
        PluginManager.unload_all()
        loggers.main.info("Saving logs")
        for _,logger in Logger._loggers.items():
            self.save_log(logger)
        self.load_thread.join()

    all_widgets_loaded: PluginEvent[()] = PluginEvent()
    "called when all widgets have loaded"
    main_widgets_loaded: PluginEvent[()] = PluginEvent()
    "called when all always visible widgets have loaded (title, version, page container, page buttons)"
    pages_initialized: PluginEvent[()] = PluginEvent()
    "called when all pages have loaded"

    def splash(self, master):
        ...

    def widgets(self, master):
        self.head_icon = (
            Label(master, text="", image=resource.image("Source", "icon.png", (50, 50)))
            .place(x=5, y=2)
            .is_literal(True)
        )

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
        
        self.main_widgets_loaded.call()

        self.page_initialize(master)
        self.splash_screen.lift()
        self.pages_initialized.call()

    def page_initialize(self, master):
        self.side_buttons = Frame(master, 50, 0, 0, 0, WidgetManager.get_color("liminal_client.root_background.color")).place(
            x=5, y=60, relheight=1
        )

        for page in pages.page.pages:
            page = page(self.main)
            if page.add_direct:
                self.add_page(page.plugin, page.key, page)

        from .pages.main import Main
        from .pages.settings import Settings

        self.main_frame: Main = WidgetManager.get_widget_by_id(
            "liminal_client.main.page"
        )[0]
        self.settings: Settings = WidgetManager.get_widget_by_id(
            "liminal_client.settings.page"
        )[0]

        self.show_page(Identifier.id("main"))

    def page_button(self, plugin: str, pageid: Identifier):
        def _page_button(pageid=pageid):
            self.page_stack.clear()
            self.show_page(pageid)
        return (
            Button(
                self.side_buttons,
                00,
                50,
                8,
                2,
                text="",
                image=resource.image(
                    plugin,
                    "pageicon/"
                    + pageid.getNamespace()
                    + "/"
                    + pageid.getPath()
                    + ".png",
                    (30, 30),
                ),
                command=_page_button,
            )
            .pack(pady=(0, 5))
            .id("pagebutton:%s.%s" % (pageid.getNamespace(), pageid.getPath()))
        )

    def add_page(self, plugin: str, id: Identifier, frame: page.Page):
        if id in self.pages.keys():
            raise Exception("Page %s already exists" % id)
        self.pages.update({(id.getNamespace() + "." + id.getPath()): frame})
        self.page_button(plugin,id)

    def show_page(self, id: Identifier):
        _id = id.getNamespace() + "." + id.getPath()
        if not _id in self.pages.keys():
            raise Exception(
                "Page %s has not been added to the pages dictionary \n%s"
                % (
                    _id,
                    "\n".join(["%s: %s" % (i[0], i[1]) for i in self.pages.items()]),
                )
            )

        if not self._current_page is None:
            if self._current_page == self.pages[_id]:
                return
            self._current_page.pack_forget()
        loggers.liminal_client.info("opening page %s", _id)
        self._current_page = self.pages[_id]
        self._current_page.pack(
            padx=(15, 65), pady=(5, 60 - 4), fill="both", expand=True
        )
        self.page_stack.push(_id)
        loggers.liminal_client.debug("Page stack: %s", self.page_stack)

    def save_log(self, log:Logger):
        import os.path
        if not os.path.exists(resource._appdata+"logs/"):
            os.mkdir(resource._appdata+"logs/")
        log.save(resource._appdata+"logs/"+log.name+".log")

    # Addon utility
    def add_color_file(self, plugin: str, file: str):
        path = os.path.join("./plugins/"+plugin+"/resources/", file)

        data = kv_file.interpret(path)

        WidgetManager.colors.update(data)
        

_instance: LiminalClient | None = None


def main():
    global _instance
    _instance = LiminalClient()
    _instance.start()
    _instance.mainloop()
    _instance.stop()


def get_instance():
    if _instance is None:
        raise Exception("Liminal Client has not been fully initialized yet")
    return _instance
