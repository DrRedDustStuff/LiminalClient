major = 3
minor = 0
release = 0
prefix = "beta"

SVG_QUALITY = 64

def version():
    return "%s.%s.%s%s" % (major, minor, release, "-" + prefix if prefix != "" else "")


import os
from blublib import kv_file
from blublib import resource

login = os.getlogin()
# Paths
downloads = ""
appdata = "C:/Users/%s/AppData/Local/LiminalClient/" % login
steamLnk = (
    "C:/Users/%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Steam/Steam.lnk"
    % login
)
etbId = 1943950
steamPath = ""
etbPath = ""
modsSuffix = "EscapeTheBackrooms/Content/Paks/--ModLoader--/"

# server
url = "https://liminal-lab.vercel.app/"

ready = False
loading_failed = False
online = True

console_enabled = False

def initialize():
    global steamPath
    global path
    global etbPath
    global ready

    steamPath = ""

    with open(steamLnk, "rb") as rbsl:
        stb = rbsl.read()
        counter = 0
        i = 0
        find = [0x6D, 0x61, 0x69, 0x6E]
        for byte in stb:
            i += 1
            if counter == 4 and byte == 0x00:
                break
            elif byte == find[counter]:
                counter += 1
            else:
                counter = 0
                path = ""
        byte = stb[i]
        while True:
            byte = stb[i]
            if byte == 0x00:
                break
            i += 1
            steamPath += str(bytes([byte]), "utf-8")
        rbsl.close()
    etbPath = (
        steamPath.removesuffix("steam.exe") + "steamapps/common/EscapeTheBackrooms/"
    )

    ready = True

    global console_enabled

    data = kv_file.interpret(resource.data("Source", "config.kv"))

    console_enabled = data["liminal_client.console_enabled.bool"] == "true"