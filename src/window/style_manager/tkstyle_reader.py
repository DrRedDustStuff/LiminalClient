from typing import Any

import platform

OSTRANSLATION: dict[str, str] = {
    "Linux":"Linux",
    "Darwin":"Mac",
    "Windows":"Windows"
}

def os_name():
    return OSTRANSLATION.get(platform.platform(), "Windows")

# key value
# element name
# - state
# - - key value

class Tag:
    value:list[str] = []

class Element:
    tags:dict[str,Tag]

def tag(text:str) -> dict[str, Tag]:
    t = text.split(": ")
    n = Tag()
    n.value = t[1].split(" ")
    return {t[0]: n}

class TKStyle:
    def __init__(self, path:str) -> None:
        self._text = ""
        with open(path, "r") as f:
            self._text = f.read()
            f.close()

        self._data:dict[str, Tag|Element] = {}

    def load(self):
        tmp: dict[str, list[str]] = {"":[]}
        parent = ""

        for line in self._text.split("\n"):
            if line.strip() == "": continue
            print("loading style line '"+ line +"'")
            if line.startswith("elem ") and line.endswith(":"):
                parent = line[5:-1]
                tmp.update({parent:[]})
            elif line.startswith("\t"):
                tmp[parent].append(line.strip())
            else:
                parent = ""
                tmp[parent].append(line.strip())

        if tmp == {"":[""]} or tmp == {"":[]}: raise RuntimeError("Loading Error")

        for elem in tmp[""]: self._data.update(tag(elem))

        for p, elem_list in tmp.items():
            if p == "": continue
            self._data.update({p:Element()})
            for elem in elem_list:
                self._data[p].tags.update(tag(elem)) # type: ignore

        return self
    
    def __getattribute__(self, name: str) -> Any:
        if name in {
            "_text", 
            "_data", 
            "__init__",
            "load",
            "tag",
            "element",
            "font"
            }:
            return super().__getattribute__(name)
        return self.tag(name)        

    def tag(self, t:str) -> Tag:
        t_ = self._data[t]
        if not isinstance(t_, Tag):
            raise AttributeError(f"item {t} is not a tag, use element(elem, tag) instead")
        return t_
    
    def element(self, e:str, t:str) -> Tag:
        e_ = self._data[e]
        if not isinstance(e_, Element):
            raise AttributeError(f"item {e} is not an element, use tag(tag) instead")
        return e_.tags[t]
    
    def font(self, t:str="font"):
        f = tuple(self.tag(t).value)
        match len(f):
            case 1: return (f[0], 16)
            case 2: return (f[0], int(f[1]))
            case 3: return (f[0], int(f[1]), f[2])
            case _: raise AttributeError(r"Not implemented ¯\_(ツ)_/¯")