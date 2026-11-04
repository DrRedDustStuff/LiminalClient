from .page import Page

from blublib.ui.ui_manager import WidgetManager
from customtkinter import CTkFont, DoubleVar
from blublib.ui.widgets import Label, OptionMenu, Frame, Button, Switch, Slider
from typing import Any, Callable, Literal, TypeAlias, cast

from blublib.ui.labeled_slider import LabeledSlider
from blublib import sound
from blublib import resource
from blublib import log
from blublib.plugin.plugin_event import PluginEvent
from blublib.resource import Identifier
import json
import os

SettingsWidgetType: TypeAlias = Literal[
    "slider",
    "switch",
    "dropdown",
]


def category(id: Identifier):
    return id.getNamespace() + "." + id.getPath() + ".category.frame"


class Settings(Page):
    key = Identifier.id("settings")
    load_settings: PluginEvent = PluginEvent()

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

        logging_category = Identifier.id("logging")
        self.category(logging_category)
        self.header(Identifier.id("logging"), logging_category)
        self.dropdown(
            Identifier.id("logging_level"),
            [
                "Debug",
                "Info",
                "Warn",
                "Error",
                "Critical",
            ],
            lambda val: log.Logger.set_level(cast(log.Level,val)),
            logging_category
        )

        debug_category = Identifier.id("debug")
        self.category(debug_category)
        self.header(Identifier.id("debug"), debug_category)

        Settings.load_settings.call()

        

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
            .id(varname)
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
        for id, val in self.settings.copy().items():
            namespace, name, type = id.split(".", 2)
            type = cast(SettingsWidgetType, type)
            if type == "dropdown":
                t = "optionmenu"
            else:
                t = type
            try:
                settings_widget = WidgetManager.get_widget_by_id(
                    "%s.%s.%s" % (namespace, name, t)
                )[0]
            except Exception as e:
                log.error("%s: %s", e.__class__.__name__,str(e))
                self.settings.pop(id)
                continue
            match type:
                case "slider":
                    slider: Slider = settings_widget
                    slider.set(float(val))
                    if slider._command is not None:
                        slider._command(float(val))
                case "dropdown":
                    dropdown: OptionMenu = settings_widget
                    dropdown.set(val)
                    if dropdown._command is not None:
                        dropdown._command(val)
                case "switch":
                    print(val)
                    zwitch: Switch = settings_widget
                    zwitch.configure(False, variable=bool(val))
                    if zwitch._command is not None:
                        zwitch._command(bool(val))

    def save(self):
        with open(resource.datapath("settings.json"), "w", encoding="utf-8") as wsf:
            json.dump(self.settings, wsf)
            wsf.close()
