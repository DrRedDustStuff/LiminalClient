from .page import Page

from blublib.ui.ui_manager import WidgetManager
from customtkinter import CTkFont, DoubleVar
from blublib.ui.widgets import Label, OptionMenu, Frame, Button, Switch, Slider
from typing import Any, Callable, Literal, TypeAlias, cast

from blublib.ui.labeled_slider import LabeledSlider
from blublib import sound
from blublib import resource
from blublib.resource import Identifier
import json
import os

SettingsWidgetType: TypeAlias = Literal["slider", "switch"]


def category(id: Identifier):
    return id.getNamespace() + "." + id.getPath() + ".category.frame"


class Settings(Page):
    key = Identifier.id("settings")

    def __init__(self, parent):
        super().__init__(parent)
        self.settings: dict[str, Any] = {}

    def widgets(self):
        self.header(Identifier.id("settings"), None)

        general_category = Identifier.id("general")
        self.category(general_category)
        self.header(Identifier.id("general"), general_category)
        self.dropdown(
            Identifier.id("lang_sett"),
            [
                "English",
                "Deutsch",
            ],
            lambda lang: WidgetManager.translate(WidgetManager.language_keys[lang]),
            general_category,
        )

        sound_category = Identifier.id("sound")
        self.category(sound_category)
        self.header(Identifier.id("sound"), sound_category)
        self.slider(
            Identifier.id("notification"),
            Identifier.id("notification"),
            lambda x: None,
            sound_category,
        )
        self.switch(
            Identifier.id("TEST"), Identifier.id("TEST"), lambda x: None, sound_category
        )

    def category(self, id: Identifier, parent: Identifier | None = None):
        frame = (
            Frame(
                (self if parent is None else self.get_parent(parent)),
                border_width=2,
                corner_radius=8,
            )
            .id(Identifier.get(id.getNamespace(), id.getPath() + ".category"))
            .pack(padx=0, pady=5, fill="x")
        )

    def header(self, text: Identifier, parent: Identifier | None):
        header = Label(
            (self if parent is None else self.get_parent(parent)),
            text=text.pathSuffix("header"),
            font=CTkFont(None, 24, "bold"),
        ).pack(padx=10, pady=5, fill="x")

    def switch(
        self,
        text: Identifier,
        varname: Identifier,
        command: Callable[[bool], Any],
        parent: Identifier,
    ):
        switch = (
            Switch(
                self.get_parent(parent),
                text=text.pathPrefix("setting"),
            )
            .pack(padx=10, pady=5, anchor="w")
            .id(varname)
        )

        def _command(value):
            self.settings.update(
                {"%s.%s.switch" % (varname.getNamespace(), varname.getPath()): value}
            )
            command(value)

        switch.configure(command=lambda: _command(switch.get() == 1))

    def slider(
        self,
        text: Identifier,
        varname: Identifier,
        command: Callable[[float], Any],
        parent: Identifier,
    ):
        def _command(value: float):
            self.settings.update(
                {"%s.%s.slider" % (varname.getNamespace(), varname.getPath()): value}
            )
            command(value)

        slider = LabeledSlider(
            self.get_parent(parent),
            text=text.pathPrefix("setting"),
        ).pack(padx=10, pady=5, anchor="w")
        slider.slider.id(varname)

        slider.slider.configure(command=_command)

    def button(self, text: Identifier, command: Callable, parent: Identifier):
        button = Button(
            self.get_parent(parent),
            text=text.pathPrefix("setting"),
            command=command,
        ).pack(padx=10, pady=5, anchor="w")

    def dropdown(
        self,
        varname: Identifier,
        vars: list[str],
        command: Callable[[str], Any],
        parent: Identifier,
    ):
        "vars only literal"
        dropdown = (
            OptionMenu(
                self.get_parent(parent),
                values=vars,
            )
            .pack(padx=10, pady=5, anchor="w")
            .is_literal(True)
        )

        def _command(value: str):
            self.settings.update(
                {"%s.%s.dropdown" % (varname.getNamespace(), varname.getPath()): value}
            )
            command(value)

        dropdown.configure(command=_command)

    def get_parent(self, id: Identifier):
        return WidgetManager.get_widget_by_id(category(id))[0]

    def load(self):
        if not os.path.exists(resource.datapath("settings.json")):
            return

        with open(resource.datapath("settings.json"), "r", encoding="utf-8") as rsf:
            self.settings.update(json.load(rsf))
            rsf.close()
        for id, val in self.settings.items():
            namespace, name, type = id.split(".", 2)
            type = cast(SettingsWidgetType, type)
            try:
                settings_widget = WidgetManager.get_widget_by_id(
                    "%s.%s.%s" % (namespace, name, type)
                )[0]
            except: continue
            match type:
                case "slider":
                    slider: Slider = settings_widget
                    slider.set(float(val))
                case "switch":
                    print("is in fact a switch")

    def save(self):
        with open(resource.datapath("settings.json"), "w", encoding="utf-8") as wsf:
            json.dump(self.settings, wsf)
            wsf.close()
