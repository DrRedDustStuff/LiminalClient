
import requests, shutil, os, sys
import win32com.client
import pythoncom
from customtkinter import DoubleVar, CTkLabel
from tkinter import LabelFrame
from time import sleep, time

app_data = f"C:/Users/{os.getlogin()}/AppData/"

OWNER = "DrRedDustStuff"
REPO = "LiminalClient"

# Optional: add token for private repos
HEADERS = {
}

OFFLINE = False

last_error = "NoError"

progress = DoubleVar()
info_container = LabelFrame()
def download_step(p:float, prefix:str, description:str, color:str="white"): ...

def download(location:str) -> str:
    sleep(0.1)
    global last_error
    if not OFFLINE:
        download_step(0.05, "Github", "Pinging Github")
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        download_step(0.1, "Github", "got Github response")

        asset = data["assets"][0]
        download_step(0.2, "Github", "getting zip asset")
        download_url = asset["url"]
        download_step(0.3, "Github", "getting zip download url")

        download_headers = {
            **HEADERS,
            "Accept": "application/octet-stream"
        }

        download_step(0.35, "Github", "requesting zip file")
        start_time = time()
        r = requests.get(download_url, headers=download_headers)

        download_step(0.45, "Github", f"Response took {time() - start_time}s")
        download_step(0.4, "Github", "Got content bytes")
        content = r.content
    else:
        try:
            with open("./build/Liminal Client Early access.zip", "rb") as r:
                download_step(0.4, "OFFLINE", "getting installer zip file", "green")
                content = r.read()
                r.close()
        except:
            return "InvalidOfflineMode"
    
    download_step(0.5, "Files", "Starting file creation operation")
    try:
        if os.path.exists(location): download_step(0.55, "Files", "Deleting old instance of Liminal Client", "orange"); shutil.rmtree(location)
        os.mkdir(location)
    except PermissionError as pe:
        download_step(0, "ERROR", "Permission missing")
        return "PermissionMissing"

    try:
        with open(location+"latest.zip", "wb") as f:
            f.write(content)
        download_step(0.6, "Files", "Creating zip file from gotten content", "yellow")
    except PermissionError as pe:
        download_step(0, "ERROR", "Permission missing")
        return "PermissionMissing"
    except FileNotFoundError as fnfe:
        download_step(0, "ERROR", "File not found")
        return "FileNotFound"

    shutil.unpack_archive(location+"latest.zip", location)
    download_step(0.7, "Files", "Extracting zip file", "yellow")

    try:
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(app_data+"Roaming/Microsoft/Windows/Start Menu/Programs/Liminal Client.lnk")
        
        exe_file = ""
        for file in os.listdir(location):
            if file.endswith(".exe"):
                exe_file = file
        shortcut.TargetPath = location+exe_file
        shortcut.WorkingDirectory = os.path.dirname(location)

        shortcut.save()
    except Exception as exception:
        return "ShortcutError"
    download_step(0.8, "Link", "created app menu shortcut for easier access", "cyan")

    if not os.path.exists(app_data+"Local/LiminalClient/"): download_step(0.825, "Files", "creating local appdata"); os.mkdir(app_data+"Local/LiminalClient/")
    if os.path.exists(app_data+"Local/LiminalClient/resources/"): download_step(0.875, "FIles", "creating resources folder in local appdata"); shutil.rmtree(app_data+"Local/LiminalClient/resources/")
    shutil.move(location+"resources/", app_data+"Local/LiminalClient/resources/")
    download_step(0.9, "Installation", "Moving installed resources to local appdata folder")

    with open(app_data+"Local/LiminalClient/resources/data", "x", encoding="utf-8") as cw:
        cw.write("")
        cw.close()
    download_step(0.95, "Installation", "Created/Emptied data file")
    download_step(1.0, "Installation", "Completed download!", "limegreen")
    sleep(0.4)
    return "NoError"

# def desktop_shortcut(location):
#     global last_error
#     try:
#         sys.exit()

#         pythoncom.CoInitialize()
#         shell = win32com.client.Dispatch("WScript.Shell")
#         shortcut = shell.CreateShortcut(os.path.realpath("Desktop"))
        
#         exe_file = ""
#         for file in os.listdir(location):
#             if file.endswith(".exe"):
#                 exe_file = file
#         shortcut.TargetPath = location+exe_file
#         shortcut.WorkingDirectory = os.path.dirname(location)

#         shortcut.save()
#         last_error = "NoError"
#     except Exception as exception:
#         last_error = "ShortcutError"
#         print(exception)
