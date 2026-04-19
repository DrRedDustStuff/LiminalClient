from src import data
import datagen
import sys

# Data
TEMPPATH = "./build/temp"
DISTPATH = "./build"

CLEAR_CACHE = True
ONEFILE = True

SPECPATH = "./build"

APPNAME = "Liminal Client" + (" Installer" if sys.argv[2] == "installer" else "")
APPICON = "../resources/icon.ico"

ZIP_POSTFIX = "Early access"

RESOURCES_PATH = "resources"
REMOVE_FROM_RESOURCES = ["data"]

with open("./build/version.txt", "r", encoding="utf-8") as r:
  version = r.read()
  r.close()
with open("./build/_version.txt", "w", encoding="utf-8") as w:
  w.write((version
    .replace(r"{appname}", APPNAME)
    .replace(r"{exename}", APPNAME+" "+data.version)
    .replace(r"{data.major}", str(data.major))
    .replace(r"{data.minor}", str(data.minor))
    .replace(r"{data.build}", str(data.build))
    .replace(r"{data.revision}", str(data.revision))
    ))
  w.close()

EXCLUDE_IMPORTS = [
   
]

import subprocess

ei = []
[(ei.append("--exclude-module"), ei.append(name)) for name in EXCLUDE_IMPORTS]

command = ["pyinstaller",
    sys.argv[1],
    "--clean" if CLEAR_CACHE else None,
    "--version-file", "./_version.txt",
    "--distpath", DISTPATH,
    "--workpath", TEMPPATH,
    "--onefile" if ONEFILE else None,
    "--specpath", SPECPATH,
    "--name", APPNAME+(" "+data.version if sys.argv[2] == "app" else ""),
    "--icon", APPICON,
    "--windowed",
    "--uac-admin" if sys.argv[2] == "installer" else None,
    *ei
    ]

while None in command:
  command.remove(None)

print(command)
subprocess.call(command)

import shutil, os

if sys.argv[2] == "app":

  if os.path.exists(f"build/{APPNAME+" "+data.version}.spec"): os.remove(f"build/{APPNAME+" "+data.version}.spec")
      
  if not os.path.exists(f"build/{APPNAME}"): os.mkdir(f"build/{APPNAME}")

  shutil.move(f"build/{APPNAME+" "+data.version}.exe", f"build/{APPNAME}/{APPNAME}.exe")
  shutil.copytree(RESOURCES_PATH, f"build/{APPNAME}/{RESOURCES_PATH}")

  for dir in REMOVE_FROM_RESOURCES:
      if os.path.exists(f"build/{APPNAME}/{RESOURCES_PATH}/{dir}"):
          os.remove(f"build/{APPNAME}/{RESOURCES_PATH}/{dir}")

  shutil.make_archive(APPNAME, "zip", f"build/{APPNAME}/")
  shutil.move(f"{APPNAME}.zip", f"build/{APPNAME if ZIP_POSTFIX == "" else APPNAME + " " + ZIP_POSTFIX}.zip")

  shutil.rmtree(f"build/{APPNAME}/")

elif sys.argv[2] == "installer":

  if os.path.exists(f"build/{APPNAME}.spec"): os.remove(f"build/{APPNAME}.spec")
      
  if not os.path.exists(f"build/{APPNAME}"): os.mkdir(f"build/{APPNAME}")

  shutil.move(f"build/{APPNAME}.exe", f"build/{APPNAME}/{APPNAME}.exe")

  shutil.make_archive(APPNAME, "zip", f"build/{APPNAME}/")
  shutil.move(f"{APPNAME}.zip", f"build/{APPNAME}.zip")

  shutil.rmtree(f"build/{APPNAME}/")
