from typing import Any

from customtkinter import CTk, CTkFont
import customtkinter as ctk

from .ui.widgets import (
    Frame,
    ScrollableFrame,
    Label,
    Entry,
    Button,
    Slider,
)
from .ui.mod_display import ModDisplay
from .ui.ui_manager import WidgetManager
from .datafile import Datafile
from . import data, resource, log, sound
from .exceptions import UnhandledCase

from tkinter import PhotoImage

from threading import Thread

import requests
import time


def ping_server():
    try:
        response = requests.get(data.url, timeout=3)
        if response.ok:
            data.online = True
        else:
            raise Exception(response.text)
    except requests.exceptions.Timeout as te:
        data.online = False
        print(te)
    except requests.exceptions.ConnectionError as ce:
        data.online = False
        print(ce)


def lerp(a: float, b: float, delta: float):
    return a + (b - a) * delta


def ease(a: float, b: float, delta: float):
    return a + (b - a) * (delta * delta * (3 - 2 * delta))


class LiminalClient:
    card_queue: list[tuple[str, str, str]] = []

    def load(self):
        data.initialize()
        ping_server()
        if not data.online:
            self.card(
                "Offline",
                "it seems we could not reach the Liminal Labs server",
                "#DBB449",
            )
        self.ready = True

    def card(self, title: str, text: str, color: str):
        self.card_queue.append((title, text, color))

    def _info_card(self, header: str, text: str, color: str):
        self.can_que = False
        frame = Frame(self.tk, 250, 150, corner_radius=8, fg_color="#3A3A3A")
        Frame(frame, 250, 32, corner_radius=8, fg_color=color).place(x=0, y=0)
        Frame(frame, 250, 24, fg_color="#3A3A3A").place(x=0, y=16)
        Label(
            frame, 250, 24, text=header, font=CTkFont(None, 24, "bold"), anchor="w"
        ).place(x=20, y=16)
        Label(
            frame,
            250,
            25,
            text=text,
            wraplength=200,
            anchor="nw",
            justify="left",
            compound="left",
        ).place(x=10, y=52)

        sound.notification(sound.swoosh)
        self.info_card_in(
            frame, 0, -0.5, (self.tk.winfo_height() - 4) / self.tk.winfo_height()
        )

    def info_card_in(self, card: Frame, time: float, relx: float, y: float):
        rx = ease(relx, 0, 0.1)
        card.place_configure(relx=rx, rely=y, x=2, anchor="sw")
        if rx > -0.001:
            self.info_card_hold(card, 2, y)
            return
        self.tk.after(10, lambda: self.info_card_in(card, time + 0.01, rx, y))

    def info_card_hold(self, card: Frame, timeout: float, y: float):
        tm = timeout - 0.01
        if tm <= 0.001:
            self.can_que = True
            self.info_card_out(card, 0, 0, y)
            return
        self.tk.after(10, lambda: self.info_card_hold(card, tm, y))

    def info_card_out(self, card: Frame, time: float, relx: float, y: float):
        rx = ease(relx, -0.5, 0.1)
        card.place_configure(relx=rx, rely=y, x=2, anchor="sw")
        if rx < -0.499:
            card.destroy()
            return
        self.tk.after(10, lambda: self.info_card_out(card, time + 0.01, rx, y))

    def run_card_queue(self):
        if len(self.card_queue) > 0 and self.can_que:
            title, text, color = self.card_queue.pop(0)
            self._info_card(title, text, color)
        self.tk.after(10, self.run_card_queue)

    def __init__(self) -> None:
        ctk.set_default_color_theme("./resources/theme.json")
        WidgetManager.load_theme()
        self.can_que = True

        self.tk = CTk()
        self.tk.geometry(f"1200x800")
        self.tk.minsize(1200, 800)
        self.tk.resizable(True, True)
        self.tk.iconbitmap(default=resource.path("image/icon.ico"))
        self.tk.title("Liminal Client")

        self.ready = False
        self.load_thread = Thread(target=self.load)
        self.load_thread.start()

        self.pages: dict[str,ScrollableFrame] = {}
        self._current_page:ScrollableFrame|None = None

        self.widgets(self.tk)
        WidgetManager.translate("en_us")
        self.run_card_queue()
        self.tk.after(
            10,
            lambda: self.card(
                "Beta, (%s)" % (data.version()),
                "Thank you for using the beta version of Liminal Client! Please report any bugs or errors to the Liminal Labs team.",
                "#4FF02F",
            ),
        )
        self.tk.mainloop()
        self.load_thread.join()

    def widgets(self, master):
        self.main_header = Label(
            master, text="Liminal Client", font=CTkFont(None, 30, "bold")
        ).place(y=4, x=100).is_literal(True)

        self.version_label = Label(
            master,
            text_color="#969696",
            text=f"v:" + data.version(),
            font=CTkFont(None, 14, "normal", "italic")
        ).place(y=12, x=300).is_literal(True)

        self.main = Frame(master, corner_radius=24, border_width=3)
        self.main.place(x=60, y=50, relwidth=1, relheight=1)
        self._settings()
        self._main()

        self.page_buttons(master)

    def page_buttons(self,master):
        self.show_page("settings")
        self.show_page("main")

        self.side_buttons = Frame(
            master, 50, 0, 0, 0, fg_color="#000000"
        ).place(x=5,y=60,relheight=1)

        def page_button(pageid:str,image:str="folder"):
            return Button(self.side_buttons,00,50,8,2,text="",image=resource.image(image+".png",(30,30)), command=lambda:self.show_page(pageid)).pack(pady=(0,5)).id("pagebutton_%s"%pageid)

        page_button("main", "home")
        page_button("settings", "settings")

    def show_page(self,id:str):
        if id in self.pages.keys():
            if not self._current_page is None:
                if self._current_page == self.pages[id]: return
                self._current_page.pack_forget()
            log.info("opening page %s",id)
            self._current_page = self.pages[id]
            self._current_page.pack(padx=(15, 65), pady=(5, 60-4), fill="both", expand=True)
        else:
            # load from guessing
            log.info("this page is not in pages %s",self.pages)
            if hasattr(self,id+"_frame"):
                self.pages.update({id:getattr(self,id+"_frame")})
                log.info("retry:")
                self.show_page(id)
            else: raise UnhandledCase()

    def _settings(self):
        self.settings_frame = ScrollableFrame(
            self.main,corner_radius=0,fg_color=self.main.cget("fg_color")
        ).tag("settings")
        self.settings_frame.pack(padx=(15, 65), pady=(5, 60-4), fill="both", expand=True)

        root = self.settings_frame

        header = Label(root,
            text="liminal_client.settings_header.label", font=CTkFont(None,42,"bold")
        ).pack(padx=20,pady=10)

        sound_category = Frame(root, border_width=2, corner_radius=8).pack(padx=0,pady=5,fill="x")
        sound_category.pack_propagate(False)
        def _(x:float):
            sound.notification_channel.set_volume(x/100)
        notification_volume = Slider(sound_category, border_width=2, width=400, from_=0,to=50,number_of_steps=100,command=_).pack(padx=25,pady=10,anchor="w")

    def _main(self):
        self.main_frame = ScrollableFrame(
            self.main, corner_radius=0, fg_color=self.main.cget("fg_color")
        ).tag("main")
        self.main_frame.pack(padx=(15, 65), pady=(5, 60-4), fill="both", expand=True)

        root = self.main_frame

        header = Frame(root).pack(pady=(2,0),fill="x", expand=True)
        run_game_button = Button(
            header,
            text="liminal_client.run_game.button",
            width=0,
            height=42,
            font=CTkFont(None, 16, "bold"),
            image=resource.image("round-play.png"),
        ).pack(side="right", pady=12, padx=4)

        mods_header = Label(
            root, text="liminal_client.mods_header.label", font=CTkFont(None, 42, "bold")
        ).pack(padx=20, pady=10)
        hero = Frame(root).pack(fill="x", expand=True)

        upload_files = Button(
            hero, 130, text="liminal_client.upload_files.button", image=resource.image("folder-plus.png")
        ).pack(side="right", padx=2)

        browse_content = Button(
            hero,
            140,
            text="liminal_client.browse_content.button",
            state="disabled",
            image=resource.image("compass.png"),
        ).pack(side="right", padx=2)

        mod_search = Entry(
            hero, placeholder_text="liminal_client.mod_search.entry"#, state="disabled"
        ).pack(side="left", fill="x", expand=True, padx=2)

        mods_frame = Frame(
            root, corner_radius=12, height=400, fg_color=WidgetManager.color("mods_frame"), border_width=3
        ).pack(padx=2, pady=(18, 12), fill="both", expand=True)

        self.footer = Frame(
            root, corner_radius=0, height=100, fg_color="transparent"
        ).pack(padx=0, pady=(12, 2), fill="x", expand=True)

        self._footer_left()
        self._footer_middle()
        self._footer_right()

    def _footer_left(self):
        self.footer_left = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=0, relwidth=(1 / 3), anchor="nw", relheight=1)

        self._footer_text(
            self.footer_left, "liminal_client.credit.head", "liminal_client.credit.creator", "."
        )

    def _footer_middle(self):
        self.footer_middle = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=(1 / 3), relwidth=(1 / 3), anchor="nw", relheight=1)
        self._footer_text(self.footer_middle, "liminal_client.about.head", ".")

    def _footer_right(self):
        self.footer_right = Frame(
            self.footer, corner_radius=0, fg_color="transparent"
        ).place(relx=(2 / 3), relwidth=(1 / 3), anchor="nw", relheight=1)
        self._footer_text(self.footer_right, "liminal_client.help.head", ".")

    def _footer_text(self, root, head: str, *texts: str):
        Label(root, text=head, font=CTkFont(None, 16, "bold")).pack(
            side="top", anchor="n", padx=10, pady=(10, 0)
        )
        for text in texts:
            Label(root, text=text).pack(side="top", anchor="n", padx=10, pady=(5, 0))


def main():
    LiminalClient()
