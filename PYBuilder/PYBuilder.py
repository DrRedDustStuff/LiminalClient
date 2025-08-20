import json
import subprocess
import os
import shutil
import time

def build(path:str,dst_name=None, onefile=True, icon=None, windowed=True):
    st = time.time()
    command = ['pyinstaller']
    command.append('--onefile') if onefile else None
    command.append('--windowed') if windowed else None
    command.append(f'--icon={icon}') if icon else None
    command.append(f'--name={dst_name}') if dst_name else None
    command.append(path)
    subprocess.run(command, check=True)
    os.remove(f"./{dst_name}.spec")
    shutil.rmtree("./build/", True)
    print(f"[Sub] [PYBuilder] done in {time.time() - st}s")


jsn: dict = json.loads(open("./PYBuilder/build.json").read())
path:str = jsn.get("script", "")
name:str = jsn.get("save-as", "")
icon:str = jsn.get("icon-file", "")
windowed:bool = bool(jsn.get("gui"))
build(path, name, True, icon, windowed)

exit(0)
