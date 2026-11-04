import sys

from tkinter import filedialog, messagebox
from customtkinter import CTk, CTkFont, DoubleVar
import customtkinter as ctk
from customtkinter import (
    CTkLabel,
    CTkProgressBar,
    CTkFrame,
    CTkButton,
    CTkOptionMenu,
    CTkEntry,
    CTkImage,
)

from blublib.log import Logger

from blublib import resource
from blublib.resource import Identifier

from threading import Thread
import requests

import os
import errno
import json
import shutil
import zipfile
import time
import pythoncom
from win32com.client import Dispatch

import asyncio
import threading

def subthread(func):
    thread = threading.Thread(target=func, daemon=True)
    thread.start()
    return thread

from blublib import svg_images

TEMP_ZIP_POS = "C:/tmp/temp_zip.zip"

SIZE = (32,32)
ENV = {
    "currentColor": "#FFFFFF"
}
GENERATE = False
ICON = {
    "Home": None if not GENERATE else svg_images.direct_generate(
        """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-home">
<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
<polyline points="9 22 9 12 15 12 15 22"></polyline>
</svg>""",
        SIZE,
        ENV,
    ),
    "Settings": None if not GENERATE else svg_images.direct_generate(
        """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-settings">
<circle cx="12" cy="12" r="3"></circle>
<path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path>
</svg>
""",
        SIZE,
        ENV,
    ),
    "Install": None if not GENERATE else svg_images.direct_generate(
        """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-download">
<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
<polyline points="7 10 12 15 17 10"></polyline>
<line x1="12" y1="15" x2="12" y2="3"></line>
</svg>
""",
        SIZE,
        ENV,
    ),
    "Finish": None if not GENERATE else svg_images.direct_generate(
        """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-power">
<path d="M18.36 6.64a9 9 0 1 1-12.73 0"></path>
<line x1="12" y1="2" x2="12" y2="12"></line>
</svg>
""",
        SIZE,
        ENV,
    )
}


class Installer:
    def __init__(self) -> None:
        self.tk = CTk()

        self.FONT = CTkFont("Helvetica")
        self.BOLD_FONT = CTkFont("Helvetica", weight="bold")

        self.setup()
        self.widgets()
        self.load_file()


        self.page_home()

    def load_file(self):
        if len(sys.argv) == 2:
            self.path = sys.argv[1]
        else:
            self.path = "data.dlf"

        if not os.path.exists("C:/tmp/"):
            os.mkdir("C:/tmp/")

        rdlf = open(self.path, "rb")
        data = rdlf.read()
        rdlf.close()

        if data[0:3] != b"DLF":
            raise Exception("File is not a valid download file")

        data_length = int.from_bytes(data[3:7])
        zip_length = int.from_bytes(data[7:11])

        self.data: dict[str, str] = json.loads(data[11 : 11 + data_length].decode())
        self.zipdata = data[11 + data_length : 11 + data_length + zip_length]

        print(self.data)

        wzd = open(TEMP_ZIP_POS, "wb")
        wzd.write(self.zipdata)
        wzd.close()

        self.app_name = self.data["name"]
        self.destination_path = self.data["default_directory"]
        self.description = "\n".join(self.data["description"])
        self.finish_page = "\n".join(self.data["finish_page"])
        self.options = self.data["options"]

        self.tk.title("Installer - " + self.app_name)

    def setup(self):
        self.tk.resizable(False, False)
        self.tk.geometry("600x450")
        self.tk.title("Installer - Loading...")

    def widgets(self):
        self.main_frame = CTkFrame(self.tk)
        self.main_frame.pack(fill="both", side="right", expand=True, padx=1, pady=2)

        self.pages_frame = CTkFrame(self.tk, 80)
        self.pages_frame.pack(fill="y", side="left", padx=1, pady=2)

        self.page_labels: dict[str, CTkLabel] = {}

        if GENERATE:
            for name in ["Home", "Settings", "Install", "Finish"]:
                icon = ICON[name]

                label = CTkLabel(self.pages_frame, 32,32, text="", image=CTkImage(icon,icon, (32,32))) # pyright: ignore[reportArgumentType]
                label.pack(padx=4,pady=4)

                self.page_labels.update({name: label})
        else:
            for name in ["Home", "Settings", "Install", "Finish"]:
                label = CTkLabel(self.pages_frame, 32,32, text=name) # pyright: ignore[reportArgumentType]
                label.pack(padx=4,pady=4)

                self.page_labels.update({name: label})

    def set_label(self, name: str):
        for k,v in self.page_labels.items():
            if k == name:
                v.configure(font=self.BOLD_FONT)
            else:
                v.configure(font=self.FONT)

    def unpack_zip(self):
        if not zipfile.is_zipfile(TEMP_ZIP_POS):
            raise Exception("Zip file did not generate correctly")

        zip = zipfile.ZipFile(TEMP_ZIP_POS, "r")
        # zip.open(TEMP_ZIP_POS, "r")
        members = zip.namelist()

        path = os.fspath(self.destination_path)

        def unpack_member(i, zipinfo):
            member = zip.NameToInfo.get(zipinfo)
            if member is None:
                raise KeyError("There is not item named %r in the archive" % member)

            self.extract_member(zip, member, path)
            self.extract_progress.set(i / len(members))

            self.extract_steps.configure(text=member.filename+"\n"+self.extract_steps.cget("text"))
            self.extract_steps.configure(text="\n".join(self.extract_steps.cget("text").split("\n")[0:24]))

        for i,k in enumerate(members):
            unpack_member(i,k)
            # time.sleep(0.001)

    def extract_member(self, zip: zipfile.ZipFile, member: zipfile.ZipInfo, targetpath):
        arcname = member.filename.replace("/", os.path.sep)

        if os.path.altsep:
            arcname = arcname.replace(os.path.altsep, os.path.sep)
        arcname = os.path.splitdrive(arcname)[1]
        invalid_path_parts = ("", os.path.curdir, os.path.pardir)
        arcname = os.path.sep.join(
            x for x in arcname.split(os.path.sep) if x not in invalid_path_parts
        )

        if not arcname and not member.is_dir():
            raise ValueError("Empty filename.")

        targetpath = os.path.normpath(os.path.join(targetpath, arcname))

        # Create all upper directories if necessary.
        upperdirs = os.path.dirname(targetpath)
        if upperdirs and not os.path.exists(upperdirs):
            os.makedirs(upperdirs, exist_ok=True)

        if member.is_dir():
            if not os.path.isdir(targetpath):
                try:
                    os.mkdir(targetpath)
                except FileExistsError:
                    if not os.path.isdir(targetpath):
                        raise
            return targetpath
        
        with zip.open(member) as source, open(targetpath, "wb") as target:
            shutil.copyfileobj(source, target)

        return targetpath

    def install(self):
        time.sleep(0.25)
        print("Unpacking")
        self.unpack_zip()
        print("Done")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        start_menu = os.path.join(self.destination_path,"Liminal Client.exe")
        link_name = "C:/Users/%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Liminal Client.lnk"%os.getlogin()
        
        pythoncom.CoInitialize()
        shell = Dispatch("WScript.Shell")
        shortcut = shell.CreateShortCut(link_name)
        shortcut.Targetpath = start_menu
        shortcut.IconLocation = start_menu
        shortcut.save()  # overwrites if .lnk already exists
        pythoncom.CoUninitialize()

        time.sleep(3)
        self.tk.after(5, self.page_finish)

    def start(self):
        self.tk.mainloop()
        return self

    def clear(self):
        for child in self.main_frame.winfo_children():
            child.destroy()

    def page_home(self):
        self.clear()
        self.set_label("Home")

        header = CTkLabel(
            self.main_frame, text=self.app_name, font=("Helvetica", 24, "bold")
        )
        header.pack(fill="x", pady=4)

        description = CTkLabel(
            self.main_frame,
            text=self.description,
            font=("Helvetica", 14),
            wraplength=500,
            anchor="nw",
        )
        description.pack(fill="both", expand=True, pady=8, padx=40)

        next_page = CTkButton(self.main_frame, text="Next", command=self.page_settings)
        next_page.pack(anchor="se", side="bottom", padx=4,pady=4)

    def page_settings(self):
        self.clear()
        self.set_label("Settings")

        header = CTkLabel(
            self.main_frame, text="Settings", font=("Helvetica", 24, "bold")
        )
        header.pack(fill="x", pady=4)

        self.path_input = CTkEntry(self.main_frame)
        self.path_input.pack(fill="x", pady=(4,1),padx=5)

        def _select_path():
            path = filedialog.askdirectory()
            if path == "": return
            self.destination_path = path
            self.path_input.delete("0","end")
            self.path_input.insert("insert", self.destination_path)
        select_path = CTkButton(self.main_frame, text="Select path", command=_select_path)
        select_path.pack(fill="x", pady=1,padx=5)

        def attempt_install():
            self.destination_path = self.path_input.get()
            # if not os.path.exists(self.path_input.get()):
            #     messagebox.showerror("Invalid path", "The destination path '%s' is not a valid destination."%self.path_input.get())
            #     return
            self.page_install()

        next_page = CTkButton(self.main_frame, text="Install", command=attempt_install)
        next_page.pack(anchor="se", side="bottom", padx=4,pady=4)

        self.path_input.delete("0", "end")
        self.path_input.insert("insert", self.destination_path)

    def page_install(self):
        self.clear()
        print(self.destination_path)
        self.set_label("Install")
        
        header = CTkLabel(
            self.main_frame, text="Installing...", font=("Helvetica", 24, "bold")
        )
        header.pack(fill="x", pady=4)

        self.extract_progress = DoubleVar(None, 0.0)
        self.progress_bar = CTkProgressBar(self.main_frame, variable=self.extract_progress)
        self.progress_bar.pack(fill="x", padx=20, pady=4)

        self.extract_steps = CTkLabel(self.main_frame)
        self.extract_steps.pack(padx=20,pady=5,fill="both")

        subthread(self.install)

    def page_finish(self):
        self.clear()
        self.set_label("Finish")
        
        header = CTkLabel(
            self.main_frame, text="Finish", font=("Helvetica", 24, "bold")
        )
        header.pack(fill="x", pady=4)

        paragraph = CTkLabel(
            self.main_frame,
            text=self.finish_page,
            font=("Helvetica", 14),
            wraplength=500,
            anchor="nw",
        )
        paragraph.pack(fill="both", expand=True, pady=8, padx=40)

        finish_page = CTkButton(self.main_frame, text="Finish", command=self.tk.destroy)
        finish_page.pack(anchor="se", side="bottom", padx=4,pady=4)


def main():
    Installer().start()
