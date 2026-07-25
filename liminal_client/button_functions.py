from . import data
from . import resource
from . import log
import os
import shutil
import subprocess
from tkinter import messagebox
from tkinter import filedialog

# from customtkinter.windows.ctk_toplevel import CTkToplevel


def run_game():
    log.info("Running Escape the Backrooms")
    subprocess.call([data.steamPath,"-applaunch",str(data.etbId)])

def run_game_offline():
    messagebox.showinfo(
        "Important!",
        "This will run the game directly without steam which due to "
        "limitations of python libraries will freeze Liminal Client. If you "
        "wish to avoid this, press Run Game instead\n" + ("-" * 79) + "\n"
        "Note: This may get removed in future updates",
    )
    cmd = [
        "%sEscapeTheBackrooms/Binaries/Win64/Backrooms-Win64-Shipping.exe"
        % data.etbPath
    ]
    subprocess.run(cmd)
