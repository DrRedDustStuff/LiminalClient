from typing import Any
import subprocess
import shutil
import os
import sys

if not os.path.exists("./zipped/"):
    os.mkdir("./zipped/")

if not os.path.exists("files"):
    os.mkdir("files")


name = "Liminal Client"


subprocess.call(
    [
        "pyinstaller",
        "main.py",
        # "-F",
        "-n",
        name,
        "-i",
        "plugins/Source/resources/image/icon.ico",
        "-w",
        # "-p", ".venv/Lib/site-packages",
        "--noconfirm",
        "--exclude-module",
        "OpenGL",
        "--exclude-module",
        "numpy",
        "--exclude-module",
        "cryptography",
        "--exclude-module",
        "charset_normalizer",
        "--exclude-module",
        "setuptool",
    ],
    env=os.environ,
)

shutil.copyfile("dist/"+name+"/"+name+".exe", "files/"+name+".exe")
if os.path.exists("files/plugins"):
    shutil.rmtree("files/plugins")
shutil.copytree("plugins","files/plugins")

shutil.make_archive(name, "zip", "./files/")

if os.path.exists("./zipped/latest"):
    shutil.rmtree("./zipped/latest")

shutil.move(name + ".zip", "./zipped/" + name + ".zip")
shutil.copytree("files","zipped/latest/")

shutil.copyfile("zipped/"+name+".zip", "installer_files/Latest.zip")

import json

oif = open("./installer_files/properties.json", "r")
properties: dict[str, str] = json.load(oif)
datafile = properties["data"]
zipfile = properties["zip"]
oif.close()

rdf = open(datafile, "rb")
data = rdf.read()
rdf.close()

rzf = open(zipfile, "rb")
zipdata = rzf.read()
rzf.close()

data_length = len(data).to_bytes(4, signed=False)
zip_length = len(zipdata).to_bytes(4, signed=False)

d = bytearray()
d += b"DLF"
d += data_length
d += zip_length
d += data
d += zipdata

wdlf = open("./zipped/"+name+".dlf", "wb")
wdlf.write(d)
wdlf.close()


