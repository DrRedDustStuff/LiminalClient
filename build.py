from liminal_client import log
from typing import Any, Callable
import subprocess
import os
import shutil

log.info("Builder!")
log.info("Loading pybuild file")
src = ""
with open("./pybuild", "r", encoding="utf-8") as rpbf:
    src = rpbf.read()
    rpbf.close()
log.info("Creating functions")

_data:dict[str,dict[str,Any]] = {
    "build":{
        "script":"main.py",
        "is_gui":False,
        "single_file":False,
        "icon":""
    },
    "misc":{
        "name":"App",
    },
}
_instructions:list[tuple] = []

_macros:dict[str,str] = {}
def _replace(i):
    if isinstance(i,str):
        for name,value in _macros.items():
            i = i.replace("![%s]"%name,value)
    return i

def sp_dat(ty:str,id:str):
    return lambda x: _data[ty].update({id:_replace(x)})

def sp_ins(*inst):
    return lambda x: _instructions.append(inst + (_replace(x),))
def dp_ins(*inst):
    return lambda x,y: _instructions.append(inst + (_replace(x),_replace(y)))

functions: dict[str,Callable[...,None]] = {}
def add(name:str,func:Callable[...,None]):
    func.__qualname__ = name
    functions.update({name:func})

def macro_def(n,v):
    _macros.update({n:v})

add("Macro",macro_def)

add("ScriptPath",sp_dat("misc","script"))
add("Name",      sp_dat("misc","name"))

add("IsGui",    sp_dat("build","is_gui"))
add("SaveAsOne",sp_dat("build","single_file"))
add("IconFile", sp_dat("build","icon"))

add("NewFolder",   sp_ins("mkdir"))
add("NewFile",     sp_ins("mkfile"))
add("CopyFile",    dp_ins("cpfile"))
add("CopyFolder",  dp_ins("cpdir"))
add("MoveFile",    dp_ins("mvfile"))
add("MoveFolder",  dp_ins("mvdir"))
add("Archive",     dp_ins("mkzip"))
add("DeleteFolder",sp_ins("dldir"))

log.info("All Functions generated!")
log.info("Running pybuild script with injected functions")

globs = {
    "_data": _data,
    "_instructions": _instructions,
    "_macros":_macros
}
exec(
    src,
    globs,
    functions
)

log.info("pybuild script ran without errors!")

command = ["pyinstaller"]
def push(x:str,condition:bool=True):
    if condition: command.append(x)

push("--onefile", _data["build"]["single_file"])
push("--windowed", _data["build"]["is_gui"])
push("--icon=%s"%(_data["build"]["icon"]),_data["build"]["icon"] != "")
push("--name=%s"%(_data["misc"]["name"]))

push("--noconfirm")
push(_data["build"]["script"])

result = subprocess.run(command)
print(result.args,result.returncode,result.stderr)


for _ in _instructions:
    instruction: str = _[0]
    args = _[1:]

    match instruction:
        case "mkdir":
            try:
                os.mkdir(args[0])
            except FileExistsError:
                log.warn("Folder %s already exists, skipping creation"%args[0])

        case "mkfile":
            try:
                with open(args[0], "x") as f: f.close()
            except FileExistsError:
                log.warn("File %s already exists, skipping creation"%args[0])

        case "cpfile":
            shutil.copy(args[0],args[1])

        case "cpdir":
            if os.path.exists(args[1]): shutil.rmtree(args[1])
            shutil.copytree(args[0],args[1])

        case "mkzip":
            shutil.make_archive(args[0], "zip", args[1])

        case "dldir":
            shutil.rmtree(args[0])

        case "mvfile":
            shutil.move(args[0],args[1])

        case "mvdir":
            shutil.move(args[0],args[1])