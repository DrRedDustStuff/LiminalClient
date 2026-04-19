
import requests, shutil, os, sys
import win32com.client
import win32api
import pythoncom
from pathlib import Path

app_data = f"C:/Users/{os.getlogin()}/AppData/"

OWNER = "DrRedDustStuff"
REPO = "LiminalClient"

# Optional: add token for private repos
HEADERS = {
    "Authorization": "token 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"  # remove if public
}

OFFLINE = True

last_error = "NoError"

def download(location:str):
    global last_error
    if not OFFLINE:
        # Step 1: get latest release
        url = f"https://api.github.com/repos/{OWNER}/{REPO}/releases/latest"
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        # Step 2: pick asset (first one or match by name)
        asset = data["assets"][0]
        download_url = asset["url"]  # IMPORTANT: this is API URL

        # Step 3: download
        download_headers = {
            **HEADERS,
            "Accept": "application/octet-stream"
        }

        r = requests.get(download_url, headers=download_headers)

        content = r.content
    else:
        try:
            with open("./build/Liminal Client Early access.zip", "rb") as r:
                content = r.read()
                r.close()
        except:
            last_error = "InvalidOfflineMode"
            return

    if os.path.exists(location): shutil.rmtree(location)
    os.mkdir(location)

    with open(location+"latest.zip", "wb") as f:
        f.write(content)

    shutil.unpack_archive(location+"latest.zip", location)

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
        last_error = "NoError"
    except Exception as exception:
        last_error = "ShortcutError"
        print(exception)

    if not os.path.exists(app_data+"Local/LiminalClient/resources/"): os.mkdir(app_data+"Local/LiminalClient/")
    if os.path.exists(app_data+"Local/LiminalClient/resources/"): shutil.rmtree(app_data+"Local/LiminalClient/resources/")
    shutil.move(location+"/resources/", app_data+"Local/LiminalClient/resources/")

    with open(app_data+"Local/LiminalClient/resources/data", "x", encoding="utf-8") as cw:
        cw.write("")
        cw.close()

def desktop_shortcut(location):
    global last_error
    try:
        sys.exit()

        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(os.path.realpath("Desktop"))
        
        exe_file = ""
        for file in os.listdir(location):
            if file.endswith(".exe"):
                exe_file = file
        shortcut.TargetPath = location+exe_file
        shortcut.WorkingDirectory = os.path.dirname(location)

        shortcut.save()
        last_error = "NoError"
    except Exception as exception:
        last_error = "ShortcutError"
        print(exception)

#desktop_shortcut("C:/Program Files/Liminal Client/Liminal Client.exe")