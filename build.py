from src import data

# Data
TEMPPATH = "./build/temp"
DISTPATH = "./build"

CLEAR_CACHE = True
ONEFILE = True

SPECPATH = "./build"

APPNAME = "Liminal Client"
APPICON = "NONE"

RESOURCES_PATH = "resources"
REMOVE_FROM_RESOURCES = ["data"]

EXCLUDE_IMPORTS = ["pygame-ce"]

import subprocess

ei = []
[(ei.append("--exclude-module"), ei.append(name)) for name in EXCLUDE_IMPORTS]

subprocess.call(["pyinstaller",
    "main.py",
    "--clean" if CLEAR_CACHE else "",
    "--distpath", DISTPATH,
    "--workpath", TEMPPATH,
    "--onefile" if ONEFILE else "",
    "--specpath", SPECPATH,
    "--name", APPNAME+" "+data.version,
    "--contents-directory", RESOURCES_PATH,
    "--icon", APPICON,
    *ei
    ])

import shutil, os

if os.path.exists(f"build/{APPNAME+" "+data.version}.spec"):
    os.remove(f"build/{APPNAME+" "+data.version}.spec")
    
if not os.path.exists(f"build/{APPNAME}"):
    os.mkdir(f"build/{APPNAME}")


shutil.move(f"build/{APPNAME+" "+data.version}.exe", f"build/{APPNAME}/{APPNAME}.exe")
shutil.copytree(RESOURCES_PATH, f"build/{APPNAME}/{RESOURCES_PATH}")

for dir in REMOVE_FROM_RESOURCES:
    if os.path.exists(f"build/{APPNAME}/{RESOURCES_PATH}/{dir}"):
        os.remove(f"build/{APPNAME}/{RESOURCES_PATH}/{dir}")

shutil.make_archive(APPNAME, "zip", f"build/{APPNAME}/")
shutil.move(f"{APPNAME}.zip", f"build/{APPNAME}.zip")

shutil.rmtree(f"build/{APPNAME}/")