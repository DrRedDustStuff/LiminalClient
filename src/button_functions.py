from . import data
import subprocess
from tkinter import messagebox
from . import loggers

def run_game():
    loggers.liminal_client.info("Running Escape the Backrooms")
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
