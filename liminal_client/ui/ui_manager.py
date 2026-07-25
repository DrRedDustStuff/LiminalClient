from .widget_type import WidgetType
from .. import resource
from .. import log
from .. import kv_file
from typing import List, Any
#from . import theme
from customtkinter import ThemeManager
import json

class WidgetManager:
    widgets: dict[int, tuple[WidgetType, list[str], list[str]]] = {}
    idx: int = 0

    @classmethod
    def get_widgets(cls):
        for k, (widget, tags, ids) in cls.widgets.items():
            yield widget, (tags if len(tags) > 0 else "all"), (
                ids if len(ids) > 0 else ""
            )

    @classmethod
    def add(cls, widget: WidgetType):
        cls.widgets.update({cls.idx: (widget, ["all"], [])})
        widget._id = cls.idx
        cls.idx += 1

    @classmethod
    def tag(cls, tag: str, w: WidgetType):
        widget, tags, ids = cls.widgets[w._id]
        tags.append(tag)
        cls.widgets[w._id] = (widget, tags, ids)

    @classmethod
    def id(cls, id: str, w: WidgetType):
        widget, tags, ids = cls.widgets[w._id]
        ids.append(id)
        cls.widgets[w._id] = (widget, tags, ids)

    @classmethod
    def get_all_widgets(cls):
        "Returns all widgets"
        for id, (widget, tags, ids) in cls.widgets.items():
            yield id, widget, tags, ids

    @classmethod
    def get_widgets_by_class(cls, c: type[WidgetType]):
        "Returns all instances of class"
        for id, (widget, tags, ids) in cls.widgets.items():
            if isinstance(widget, c):
                yield id, widget, tags, ids

    @classmethod
    def get_widgets_by_tag(cls, tag: str):
        "Returns all instances of widgets with tag"
        for id, (widget, tags, ids) in cls.widgets.items():
            if tag in tags:
                yield id, widget, tags, ids

    @classmethod
    def get_widget_by_id(cls, id: str, get_as:type[WidgetType]) -> tuple[str,Any,list[str],list[str]]:
        "Returns first instance of id"
        for _id, (widget, tags, ids) in cls.widgets.items():
            if id in ids:
                if isinstance(widget,get_as):
                    return id, widget, tags, ids
                raise Exception("Widget with id %s is not expected type '%s' but rather '%s'"%(id,get_as.__name__,(type(widget).__name__)))
        raise Exception("Widget with id %s not found"%id)

    language_keys:dict[str,str] = {
        "English":"en_us",
        "Deutsch":"de_eu",
    }
    @classmethod
    def translate(cls,lang:str):
        translation = kv_file.interpret(resource.path("lang/"+lang+".lang"))

        for id, widget, tags, ids in WidgetManager.get_all_widgets():
            if not widget._translatable: continue

            # UNREACHABLE! if translatable is true, 
            # key will alway be something, this is 
            # just to make pylance happy
            if widget._key is None: continue

            if isinstance(widget._key, List):
                if not widget._key[0] in translation.keys():
                    continue
                translated = []
                for key in widget._key:
                    translated.append(translation[key])
                widget.configure(**{widget._tc:translated})
            elif isinstance(widget._key, str):
                if not widget._key in translation.keys():
                    log.warn("Missing translatable key for '%s'"%(widget._key))
                    continue
                widget.configure(**{widget._tc:translation[widget._key]})
            else: raise Exception("Hmmmmmmmmmmmmmmmmmm. this should´nt happen...")

    theme = {}
    colors = {}
    @classmethod
    def load_theme(cls):
        cls.colors = kv_file.interpret(resource.path("theme/colors.kv"))

        with open(resource.path("theme/class.json"),"r",encoding="utf-8") as rctf:
            base_theme: dict[str,dict[str,Any]] = json.load(rctf)
            rctf.close()

        cls.theme = base_theme.copy()

        for c, properties in base_theme.items():
            for property, key in properties.items():
                if not isinstance(key,str): continue
                if key in cls.colors.keys():
                    cls.theme[c][property] = cls.colors[key]
                elif "liminal_client."+key+".color" in cls.colors.keys():
                    cls.theme[c][property] = cls.colors["liminal_client."+key+".color"]

        ThemeManager._currently_loaded_theme = "default"
        ThemeManager.theme = cls.theme

    @classmethod
    def get_color(cls,id:str):
        if id in cls.colors.keys():
            return cls.colors[id]
        elif "liminal_client."+id+".color" in cls.colors.keys():
            return cls.colors["liminal_client."+id+".color"]
        raise Exception("color id %s does not exist, perhaps it wasn't loaded?"%id)
    color = get_color