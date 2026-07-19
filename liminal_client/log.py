from typing import Any

colors = {
    "black":  "30",
    "red":    "31",
    "green":  "32",
    "yellow": "33",
    "blue":   "34",
    "magenta":"35",
    "cyan":   "36",
    "white":  "37",
    "none":   "none"
}
backgrounds = {
    "black":  "40",
    "red":    "41",
    "green":  "42",
    "yellow": "43",
    "blue":   "44",
    "magenta":"45",
    "cyan":   "46",
    "white":  "47",
    "none":   "none"
}
bolds = {
    True: "1",
    False: "none"
}
darkens = {
    True: "2",
    False: "none"
}
underlines = {
    True: "4",
    False: "none"
}

def evaluate(msg:dict[str,Any]) -> str:
    color = msg.get("color", "none")
    background = msg.get("background", "none")
    bold = msg.get("bold",False)
    underline = msg.get("underline",False)
    darken = msg.get("darken",False)
    if msg.get("header",False):
        color = "magenta"
        background = "none"
        bold = True
        darken = False

    c = colors[color]
    bg = backgrounds[background]
    b = bolds[bold]
    u = underlines[underline]
    d = darkens[darken]

    text = msg.get("text","")
    if isinstance(text,list):
        text = " ".join(text)
    elif isinstance(text,tuple):
        text = " ".join(text)
    text = str(text)

    l = [c,bg,b,u,d]
    while "none" in l: l.remove("none")

    return "\033["+ ";".join(l) +"m"+text+"\033[0m"

def text(msg:dict[str,Any]|list[dict[str,Any]]):
    if isinstance(msg, dict):
        return evaluate(msg)
    else:
        t = ""
        for m in msg:
            t += evaluate(m)
        return t
    
def message(*msg:dict[str,Any]):
    print(text(list(msg)))

def style(text:str,color:str="none",background:str="none",bold:bool=False,underline:bool=False,darken:bool=False,header:bool=False):
    return {"text":text,"color":color,"background":background,"bold":bold,"underline":underline,"darken":darken,"header":header}
