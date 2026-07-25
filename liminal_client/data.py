major = 3
minor = 0
release = 0
prefix = "beta"


def version():
    return "%s.%s.%s%s" % (major, minor, release, "-" + prefix if prefix != "" else "")


import os
import subprocess
from .datafile import Datafile

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

data = Datafile("C:/Users/%s/AppData/Local/LiminalClient/data.dat" % login)

# server
url = "https://liminal-lab.vercel.app/"

ready = False
online = True

def initialize():
    global steamPath
    global path
    global etbPath
    global ready

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
