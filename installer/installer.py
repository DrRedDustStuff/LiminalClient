from customtkinter import CTk, CTkTabview, CTkButton, CTkLabel, CTkTextbox, CTkProgressBar, DoubleVar
from customtkinter import ThemeManager, AppearanceModeTracker
from tkinter import LabelFrame

import customtkinter as ctk

import os

root = CTk()
root.geometry(f"800x600+{root.winfo_screenwidth()//2-400}+{root.winfo_screenheight()//2-300}")
root.minsize(800,600)
root.title("Liminal Client Installer")

tabs = CTkTabview(root,state="disabled")
tabs.place(relwidth=1,relheight=1)


FONT = ("Arial", 16, "bold")

# -------------------------------------------------------------------------------------- #
page0 = tabs.add("Index")

index_text = CTkLabel(page0, text=f"""
Hello {os.getlogin()}!
Welcome to the Liminal Client Installer
"""[1:-1], anchor="n", font=("Arial", 14, "bold"))
index_text.pack(padx=3,pady=5,fill="both", expand=True)

next_button0 = CTkButton(page0, text="Next", font=FONT, command=lambda:tabs.set("Installing settings"))
next_button0.pack(side="right", anchor="s", padx=2,pady=2)

# -------------------------------------------------------------------------------------- #
page1 = tabs.add("Installing settings")

CTkLabel(page1, font=FONT, text="Install location").pack(side="top", anchor="n", pady=2)
install_location = CTkTextbox(page1, activate_scrollbars=False, font=FONT, height=16, width=400)
install_location.pack(side="top", anchor="n", padx=2,pady=2)
def make_single_line(event):
    content = install_location.get("1.0","end-1c")
    install_location.delete("1.0","end")
    install_location.insert("1.0", content.split("\n")[0])
install_location._textbox.bind("<KeyRelease>",make_single_line)

install_location.insert("1.0", "C:/Program Files/Liminal Client/")

from . import download
from threading import Thread
def _dispatch():
    download.last_error = download.download(install_location.get("1.0","end-1c")+"/")
    next_button2.configure(state="normal")
def start_installing():
    tabs.set("Installing")
    Thread(target=_dispatch, daemon=True).start()

next_button1 = CTkButton(page1, text="Next", font=FONT, command=start_installing)
next_button1.pack(side="right", anchor="s")
back_button1 = CTkButton(page1, text="Back", font=FONT, command=lambda:tabs.set("Index"))
back_button1.pack(side="right", anchor="s")

# -------------------------------------------------------------------------------------- #
page2 = tabs.add("Installing")

progress = DoubleVar(root, 0.0, "download_progress")
download.progress = progress
progress_bar = CTkProgressBar(page2, variable=progress, height=15)
progress_bar.pack(side="top", padx=15, pady=10, fill="x")

info_container = LabelFrame(page2, 
        text="Download Info", 
        labelanchor="n",
        background=ThemeManager.theme["CTkFrame"]["top_fg_color"][AppearanceModeTracker.get_mode()],
        foreground=ThemeManager.theme["CTkLabel"]["text_color"][AppearanceModeTracker.get_mode()],
        bd = "0",
        highlightthickness=2,
        highlightcolor=ThemeManager.theme["CTkLabel"]["text_color"][AppearanceModeTracker.get_mode()],
        highlightbackground=ThemeManager.theme["CTkLabel"]["text_color"][AppearanceModeTracker.get_mode()],
        font=(ThemeManager.theme["CTkFont"]["family"],
              ThemeManager.theme["CTkFont"]["size"],
              ThemeManager.theme["CTkFont"]["weight"]
              ))
download.info_container = info_container
def download_step(p:float, prefix:str, description:str, color:str="white"):
    progress.set(p)
    CTkLabel(
        info_container, 
        text=prefix + ": " + description.lower(), 
        anchor="w", 
        text_color=(color if not prefix == "ERROR" else "red"),
        height=14
        ).pack(
            side="top", 
            fill="x", 
            padx=2,
            pady=0
            )

download.download_step = download_step

info_container.pack_propagate(False)
info_container.pack(padx=15, pady=15, fill="both", expand=True, ipady=6)

next_button2 = CTkButton(page2, text="Next", font=FONT, state="disabled")
next_button2.pack(side="right", anchor="s")

# -------------------------------------------------------------------------------------- #
page3 = tabs.add("Finish")

def finished():
    new = index_text._text.format(error=download.last_error)
    index_text.configure(text=new)
    tabs.set("Finish")
next_button2.configure(command=finished)

index_text = CTkLabel(page3, text="""
Thanks for installing Liminal Client
Error:{error}
"""[1:-1], anchor="n", font=("Arial", 14, "bold"))
index_text.pack(padx=3,pady=5,fill="both", expand=True)

next_button3 = CTkButton(page3, text="Finish", font=FONT, command=root.destroy)
next_button3.pack(side="right", anchor="s")

root.mainloop()