import subprocess
import shutil
import os
import sys

if not os.path.exists("./zipped/"):
    os.mkdir("./zipped/")


name = "Installer"


subprocess.call(
    [
        "pyinstaller",
        "installer.py",
        "-F",
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

shutil.move("dist/"+name + ".exe", "./zipped/" + name + ".exe")


