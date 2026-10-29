import sys

from tkinter import filedialog
from customtkinter import CTk, CTkFont
import customtkinter as ctk
from customtkinter import (
    CTkLabel,
    CTkProgressBar,
    CTkFrame,
    CTkButton,
    CTkOptionMenu,
    CTkEntry,
)

from log import Logger

from blublib import resource
from blublib.resource import Identifier

from threading import Thread
import requests

import os
import json
import shutil
import zipfile

TEMP_ZIP_POS = "C:/tmp/temp_zip.zip"


class Installer:
    def __init__(self) -> None:
        self.tk = CTk()

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
        self.description = self.data["description"]
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


    def unpack_zip(self):
        if not zipfile.is_zipfile(TEMP_ZIP_POS):
            raise Exception("Zip file did not generate correctly")

        zip = zipfile.ZipFile(TEMP_ZIP_POS, "r")
        zip.open(TEMP_ZIP_POS, "r")
        members = zip.namelist()

        path = os.fspath(self.destination_path)

        for i, zipinfo in enumerate(members):
            member = zip.NameToInfo.get(zipinfo)
            if member is None:
                raise KeyError("There is not item named %r in the archive" % member)

            files_progress = i / len(members)
            print(f"{files_progress*100:3.2f}% | {member.filename}")
            self.extract_member(zip, member, path)

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

    def start(self):
        self.tk.mainloop()
        return self

    def clear(self):
        for child in self.main_frame.winfo_children():
            child.destroy()

    def page_home(self):
        self.clear()

        header = CTkLabel(self.main_frame, text=self.app_name, font=("Helvetica", 24, "bold"))
        header.pack(fill="x", pady=4)

        description = CTkLabel(self.main_frame, text=self.description, font=("Helvetica", 14), wraplength=500, anchor="nw")
        description.pack(fill="both", expand=True, pady=8, padx=40)

    def page_settings(self):
        self.clear()

    def page_install(self):
        self.clear()

    def page_finish(self):
        self.clear()


def main():
    Installer().start()
