from typing import Callable, Any

import requests as __0
from . import data as __1
import blublib.log as __2


def _check(url_postfix: str):
    if not __1.online:
        __2.error("Tried accessing LiminalLab while offline")
        return "offline", None
    _0 = __0.get(__1.url + url_postfix)
    if not _0.ok:
        __2.error("status:%s text:%s", _0.status_code, _0.text)
        return "%s" % _0.status_code, _0

    return "", _0


def _common(url: str) -> dict[str,str]:
    _0, _1 = _check(url)
    if not _0 == "":
        return {"error": _0}
    if _1 is None:
        raise Exception("You should´nt be here!")

    return {"error": "None", "data": _1.json()}

def _binary(url: str) -> dict[str,str|bytes]:
    _0,_1 = _check(url)
    if not _0 == "":
        return {"error":_0}
    if _1 is None:
        raise Exception("You should be somewhere else")

    return {"error": "None", "data": _1.content}

def _create_common(url_creator: Callable[[Any], str]):
    return lambda x: _common(url_creator(x))

def _create_binary(url_creator: Callable[[Any], str]):
    return lambda x: _binary(url_creator(x))

def _create_static(url: str):
    return lambda: _common(url)

class table:
    def __init__(self) -> None:
        self.__functions__ = {}

    def __getattribute__(self, name: str) -> Any:
        if name.startswith("__") or name == "add":
            return super().__getattribute__(name)
        return self.__functions__[name]

    def add(self,name:str,func):
        self.__functions__.update({name:func})

ping: Callable[[], dict] = _create_static("/")

mod = table()
"""
### Table of liminal client api functions
#### methods:
- get. id: int; gives a mod data based on the given id.
- tags. tags: list[str]; gives mods based on if they have any of the tags.
- search. search: str; gives all mods matching the search.
- download. id: int; gives binary data of the mod.
"""
mod.add("get",_create_common(lambda id: "mod/get/%s" % id))
mod.add("tags",_create_common(lambda tags: "/mod/tags/%s" % ",".join(tags)))
mod.add("search",_create_common(lambda search: "mod/search/%s" % search))
mod.add("download",_create_binary(lambda id: "mod/download/%s" % id))

liminal_client = table()
"""
### Table of liminal client api functions
#### methods:
- liminal_client. url: str; gives binary zip of the provided liminal client version
- liminal_client_installer; Not implemented
- get_versions; gives all versions of liminal client on the github repo
"""
liminal_client.add("liminal_client",_create_binary(lambda url: "download/liminal-client/%s"%url))
#liminal_client.add("liminal_client_installer",_create_static("properties/liminal-client/versions"))
liminal_client.add("get_versions",_create_static("properties/liminal-client/versions"))

