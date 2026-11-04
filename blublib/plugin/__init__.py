import os

if not os.path.exists("./plugins/"):
    raise Exception("Please add a plugins folder.")