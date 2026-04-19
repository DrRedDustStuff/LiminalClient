from customtkinter import set_default_color_theme, CTk, CTkToplevel
from typing import Any
import threading
from customtkinter.windows.widgets import (
    CTkButton,
    CTkCheckBox,
    CTkComboBox,
    CTkEntry,
    CTkFrame,
    CTkGIF,
    CTkRadioButton,
    CTkLabel,
    CTkOptionMenu,
    CTkProgressBar,
    CTkScrollableFrame,
    CTkSegmentedButton,
    CTkSlider,
    CTkSwitch,
    CTkTabview,
    CTkTextbox
    )

root = CTk()
root.title("Theme editor")
root.geometry("200x300+15+15")
root.resizable(False,False)

THEME = "yellow"

theme_path = "resources/theme/" + THEME + ".json"

import time
def run():
    time.sleep(0.1)
    set_default_color_theme(theme_path)
    root.after(20,run)

run()

prev = CTkToplevel()
prev.title("Preview")
prev.geometry("1200x800+245+15")
prev.resizable(False,False)

CTkButton(prev, height=200, width=200
    ).grid(column=0,columnspan=1, row=0,rowspan=1, padx=2,pady=2)
CTkCheckBox(prev, width=200
    ).grid(column=1,columnspan=1, row=0,rowspan=1, padx=2,pady=2)
CTkComboBox(prev, width=200
    ).grid(column=2,columnspan=1, row=0,rowspan=1, padx=2,pady=2)
CTkEntry(prev, width=200
    ).grid(column=3,columnspan=1, row=0,rowspan=1, padx=2,pady=2)
CTkFrame(prev, width=200
    ).grid(column=4,columnspan=1, row=0,rowspan=1, padx=2,pady=2)
CTkGIF(prev, height=200, width=200
    ).grid(column=0,columnspan=1, row=1,rowspan=1, padx=2,pady=2)
CTkRadioButton(prev, width=200
    ).grid(column=1,columnspan=1, row=1,rowspan=1, padx=2,pady=2)
CTkLabel(prev, width=200
    ).grid(column=2,columnspan=1, row=1,rowspan=1, padx=2,pady=2)
CTkOptionMenu(prev, width=200
    ).grid(column=3,columnspan=1, row=1,rowspan=1, padx=2,pady=2)
CTkProgressBar(prev, width=200
    ).grid(column=4,columnspan=1, row=1,rowspan=1, padx=2,pady=2)
CTkScrollableFrame(prev, height=200, width=200
    ).grid(column=0,columnspan=1, row=2,rowspan=1, padx=2,pady=2)
CTkSegmentedButton(prev, width=200
    ).grid(column=1,columnspan=1, row=2,rowspan=1, padx=2,pady=2)
CTkSlider(prev, width=200
    ).grid(column=2,columnspan=1, row=2,rowspan=1, padx=2,pady=2)
CTkSwitch(prev, width=200
    ).grid(column=3,columnspan=1, row=2,rowspan=1, padx=2,pady=2)
CTkTabview(prev, width=200
    ).grid(column=4,columnspan=1, row=2,rowspan=1, padx=2,pady=2)
CTkTextbox(prev, height=200, width=200
    ).grid(column=0,columnspan=1, row=3,rowspan=1, padx=2,pady=2)

root.mainloop()